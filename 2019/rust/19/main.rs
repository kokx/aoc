use std::io::{self, BufRead};
use std::convert::TryInto;
use std::collections::VecDeque;
//use std::collections::HashSet;
//use std::cmp::max;

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

fn get_value(program : Vec<i64>, x : i64, y : i64) -> i64 {
    let mut computer = IntcodeComputer::new(program);

    computer.push_input(x);
    computer.push_input(y);

    match computer.exec() {
        Some(IntcodeResult::Finished(output)) => output[0],
        Some(IntcodeResult::WaitInput(output)) => output[0],
        None => panic!("Not working")
    }
}

fn run(line : String) {
    let program: Vec<i64> = line.split(",")
                                  .map(|s| s.parse().unwrap())
                                  .collect();

    let mut total = 0;

    for x in 0..50 {
        for y in 0..50 {
            let mut computer = IntcodeComputer::new(program.clone());

            computer.push_input(x);
            computer.push_input(y);

            match computer.exec() {
                Some(IntcodeResult::Finished(output)) => {
                    total += output[0];
                },
                Some(IntcodeResult::WaitInput(output)) => {
                    println!("WI {:?}", output);
                },
                None => panic!("Not working")
            }
        }
    }
    println!("{}", total);

    let mut lo = 100;
    let mut hi = 1000;

    let mut lasty = 0;

    let mut correctans = 0;

    loop {
        let cur = (hi + lo) / 2;

        let mut firstx = 0;

        // for line y = cur, find the first x where value = 1
        for x in (0..10000).step_by(50) {
            let val = get_value(program.clone(), x, cur);

            if val == 1 {
                firstx = x;
                break;
            }
        }
        if firstx == 0 {
            // too low
            lo = cur;
            continue;
        }
        for x in (firstx - 50)..(firstx) {
            let val = get_value(program.clone(), x, cur);

            if val == 1 {
                firstx = x;
                break;
            }
        }

        // check y - 100 and x + 100, if it is also 1, we have a match
        let val = get_value(program.clone(), firstx + 99, cur - 99);

        if val == 1 {
            hi = cur;
            correctans = (firstx * 10000) + (cur - 99);
        } else {
            lo = cur;
        }

        if cur == lasty {
            break;
        }
        lasty = cur;
    }

    println!("{}", correctans);
}
