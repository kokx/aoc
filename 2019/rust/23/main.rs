use std::io::{self, BufRead};
use std::convert::TryInto;
use std::collections::VecDeque;
//use std::collections::HashSet;
//use std::cmp::max;
//use std::cell::Cell;

fn main() {
    let stdin = io::stdin();

    for line in stdin.lock().lines() {
        run(line.unwrap());
    }
}

fn mode(modes : i64, pos : usize) -> i64 {
    let mut mode = modes;

    for _ in 0..pos {
        mode /= 10;
    }

    mode % 10
}

enum IntcodeResult {
    Finished(Vec<i64>),
    WaitInput(Vec<i64>)
}

#[derive(Debug, Clone)]
struct IntcodeComputer {
    program : Vec<i64>,
    input : VecDeque<i64>,
    ic : usize,
    relative_base : i64
}

impl IntcodeComputer {

    fn new(mut prog : Vec<i64>) -> IntcodeComputer {
        for _ in 0..10000 {
            prog.push(0);
        }

        IntcodeComputer {
            program: prog,
            input: VecDeque::new(),
            ic: 0,
            relative_base: 0
        }
    }

    fn push_input(&mut self, value : i64) {
        self.input.push_back(value);
    }

    fn param_value(&self, modes : i64, offset : usize) -> Option<i64> {
        match self.param(modes, offset) {
            Some(pos) => Some(self.program[pos]),
            _ => None
        }
    }

    fn param(&self, modes : i64, offset : usize) -> Option<usize> {
        let mode = mode(modes, offset - 1);
        let loc = self.ic + offset;

        match mode {
            1 => Some(loc),
            2 => {
                let pos = self.relative_base + self.program[loc];
                let pos : usize = pos.try_into().unwrap();

                if pos > self.program.len() {
                    return None
                }

                Some(pos)
            },
            0 => {
                let pos : usize = self.program[loc].try_into().unwrap();

                if pos > self.program.len() {
                    return None
                }

                Some(pos)
            },
            _ => None
        }
    }

    fn exec(&mut self) -> Option<IntcodeResult> {
        let mut output : Vec<i64> = Vec::new();

        loop {
            // split the op into op and mode else
            let modes = self.program[self.ic] / 100;
            let op = self.program[self.ic] % 100;

            //println!("OP: {}, modes: {}", op, modes);

            match op {
                // end of the program
                99 => return Some(IntcodeResult::Finished(output)),
                3 | 4 | 9 => {
                    // relative base adjustment
                    // input and output, with one parameter

                    match op {
                        3 => {
                            let a : usize = self.param(modes, 1)?;

                            if let Some(value) = self.input.pop_front() {
                                self.program[a] = value;
                            } else {
                                return Some(IntcodeResult::WaitInput(output));
                            }
                        },
                        4 => {
                            let a = self.param_value(modes, 1)?;
                            //println!("out: {}", a);
                            output.push(a);
                        },
                        9 => {
                            self.relative_base += self.param_value(modes, 1)?;
                            //println!("base: {}", self.relative_base);
                        }
                        _ => ()
                    }

                    self.ic = self.ic + 2;
                },
                5 | 6 => {
                    // conditional jumps, with two parameters
                    let a = self.param_value(modes, 1)?;
                    let b = self.param_value(modes, 2)?;

                    // 5: jump if not zero
                    // 6: jump if zero
                    if (a == 0 && op == 6) || (a != 0 && op == 5) {
                        self.ic = b.try_into().unwrap();
                    } else {
                        self.ic += 3;
                    }
                },
                1 | 2 | 7 | 8 => {
                    // with three parameters
                    let a = self.param_value(modes, 1)?;
                    let b = self.param_value(modes, 2)?;

                    let out = self.param(modes, 3)?;

                    self.program[out] = match op {
                        // +
                        1 => a + b,
                        // *
                        2 => a * b,
                        // <
                        7 => (a < b).try_into().unwrap(),
                        // ==
                        8 => (a == b).try_into().unwrap(),
                        // all otehr cases, just return c
                        _ => self.program[out]
                    };


                    self.ic = self.ic + 4;
                },
                _ => {
                    println!("Unkown instruction: {}", op);
                    return None;
                }
            }
        }
    }
}

#[derive(Debug,Clone)]
struct NetworkMessage {
    address: usize,
    x: i64,
    y: i64
}

impl NetworkMessage {
    fn new(address : usize, x : i64, y : i64) -> NetworkMessage {
        NetworkMessage {
            address: address,
            x: x,
            y: y
        }
    }
}

struct NetworkComputer {
    computer: IntcodeComputer,
    address: usize,
    waiting: bool
}

impl NetworkComputer {
    fn new(address : usize, program : Vec<i64>) -> NetworkComputer {
        let mut computer = IntcodeComputer::new(program);
        computer.push_input(address as i64);
        NetworkComputer {
            computer: computer,
            address: address,
            waiting: false
        }
    }

    fn step(&mut self) -> VecDeque<NetworkMessage> {
        if self.waiting {
            self.computer.push_input(-1);
        }
        match self.computer.exec() {
            Some(IntcodeResult::WaitInput(output)) => {
                self.waiting = true;

                //println!("{} {:?}", self.address, output);
                let mut output = output.into_iter().collect::<VecDeque<_>>();
                //println!("{} 2 {:?}", self.address, output);

                let mut messages = VecDeque::new();

                while !output.is_empty() {
                    let addr = output.pop_front().unwrap() as usize;
                    let x = output.pop_front().unwrap();
                    let y = output.pop_front().unwrap();

                    messages.push_back(NetworkMessage::new(addr, x, y));
                }

                messages
            },
            Some(IntcodeResult::Finished(_)) => panic!("Computer {} finished unexpectedly", self.address),
            None => panic!("Computer {} crashed unexpectedly", self.address),
        }
    }

    fn send(&mut self, message : NetworkMessage) {
        self.waiting = false;
        self.computer.push_input(message.x);
        self.computer.push_input(message.y);
    }
}

fn run(line : String) {
    let program: Vec<i64> = line.split(",")
                                  .map(|s| s.parse().unwrap())
                                  .collect();

    let mut computers = (0..50)
        .map(|address| NetworkComputer::new(address, program.clone()))
        .collect::<Vec<_>>();

    'one: loop {
        for i in 0..computers.len() {
            for message in computers[i].step() {
                if message.address == 255 {
                    println!("{}", message.y);
                    break 'one;
                }
                computers[message.address].send(message);
            }
        }
    }

    let mut computers = (0..50)
        .map(|address| NetworkComputer::new(address, program.clone()))
        .collect::<Vec<_>>();

    let mut last_nat = NetworkMessage::new(0, -1, -1);
    let mut num_waiting = 0;
    let mut lasty = -1;

    'two: loop {
        let mut all_waiting = true;
        for i in 0..computers.len() {
            all_waiting = all_waiting && computers[i].waiting;
            for message in computers[i].step() {
                if message.address == 255 {
                    last_nat = message;
                } else {
                    computers[message.address].send(message);
                }
            }
        }

        if all_waiting {
            num_waiting +=1;
        } else {
            num_waiting = 0;
        }
        if num_waiting == 2 {
            if last_nat.y == lasty {
                println!("{}", last_nat.y);
                break 'two;
            }
            lasty = last_nat.y;
            computers[0].send(last_nat.clone());
        }
    }
}
