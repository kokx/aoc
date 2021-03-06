use std::io::{self, BufRead};
use std::convert::TryInto;
use std::collections::VecDeque;
use std::cmp::max;
use std::cell::Cell;

// guess: 47780111 (too high)

fn main() {
    let stdin = io::stdin();

    for line in stdin.lock().lines() {
        run(line.unwrap());
    }
}

fn mode(modes : i32, pos : usize) -> i32 {
    let mut mode = modes;

    for _ in 0..pos {
        mode /= 10;
    }

    mode % 10
}

fn get_param(program : &Vec<i32>, mode : i32, loc : usize) -> Option<i32> {
    match mode {
        1 => Some(program[loc]),
        0 => {
            let pos : usize = program[loc].try_into().unwrap();
            if pos > program.len() {
                return None;
            }

            Some(program[pos])
        },
        _ => None
    }
}

// from https://rosettacode.org/wiki/Permutations#Rust

pub fn permutations(size: usize) -> Permutations {
    let new_size : i32 = size.try_into().unwrap();
    Permutations {
        idxs: (0..new_size).collect(),
        swaps: vec![0; size],
        i: 0
    }
}

pub struct Permutations {
    idxs: Vec<i32>,
    swaps: Vec<i32>,
    i: usize,
}

impl Iterator for Permutations {
    type Item = Vec<i32>;

    fn next(&mut self) -> Option<Self::Item> {
        if self.i > 0 {
            loop {
                if self.i >= self.swaps.len() { return None; }
                if self.swaps[self.i] < self.i.try_into().unwrap() { break; }
                self.swaps[self.i] = 0;
                self.i += 1;
            }
            let cur_swap : usize = self.swaps[self.i].try_into().unwrap();
            self.idxs.swap(self.i, (self.i & 1) * cur_swap);
            self.swaps[self.i] += 1;
        }
        self.i = 1;
        Some(self.idxs.clone())
    }
}


enum IntcodeResult {
    Finished(Vec<i32>),
    WaitInput(Vec<i32>)
}

#[derive(Debug)]
struct IntcodeComputer {
    program : Vec<i32>,
    input : VecDeque<i32>,
    ic : usize
}

impl IntcodeComputer {

    fn new(prog : Vec<i32>) -> IntcodeComputer {
        IntcodeComputer {
            program: prog,
            input: VecDeque::new(),
            ic: 0
        }
    }

    fn push_input(&mut self, value : i32) {
        self.input.push_back(value);
    }

    fn exec(&mut self) -> Option<IntcodeResult> {
        let mut output : Vec<i32> = Vec::new();

        loop {
            // split the op into op and mode else
            let modes = self.program[self.ic] / 100;
            let op = self.program[self.ic] % 100;

            match op {
                // end of the program
                99 => return Some(IntcodeResult::Finished(output)),
                3 | 4 => {
                    // input and output, with one parameter

                    match op {
                        3 => {
                            let a : usize = self.program[self.ic+1].try_into().unwrap();
                            if let Some(value) = self.input.pop_front() {
                                self.program[a] = value;
                            } else {
                                return Some(IntcodeResult::WaitInput(output));
                            }
                        },
                        4 => {
                            let a = get_param(&self.program, mode(modes, 0), self.ic+1)?;
                            //println!("out: {}", a);
                            output.push(a);
                        },
                        _ => ()
                    }

                    self.ic = self.ic + 2;
                },
                5 | 6 => {
                    // conditional jumps, with two parameters
                    let a = get_param(&self.program, mode(modes, 0), self.ic+1)?;
                    let b = get_param(&self.program, mode(modes, 1), self.ic+2)?;

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
                    let a = get_param(&self.program, mode(modes, 0), self.ic+1)?;
                    let b = get_param(&self.program, mode(modes, 1), self.ic+2)?;

                    let out : usize = self.program[self.ic+3].try_into().unwrap();

                    if out >= self.program.len() {
                        return None;
                    }

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

fn run(line : String) {
    let program: Vec<i32> = line.split(",")
                                  .map(|s| s.parse().unwrap())
                                  .collect();

    println!("Part one:");
    println!("---------");

    let mut most = 0;

    for inputs in permutations(5) {
        let mut computers = vec![];

        // inject inputs into all computers
        for input in inputs {
            let mut computer = IntcodeComputer::new(program.clone());
            computer.push_input(input);
            computers.push(computer);
        }

        let mut last_out = 0;

        for mut comp in computers {
            comp.push_input(last_out);

            if let Some(IntcodeResult::Finished(output)) = comp.exec() {
                last_out = output[0];
            }
        }

        most = max(last_out, most);
    }

    // 75228 correct
    println!("{}", most);

    println!("Part two:");
    println!("---------");

    most = 0;

    for inputs in permutations(5) {
        let mut computers = Cell::new(vec![]);

        // inject inputs into all computers
        let inputs : Vec<i32> = inputs.iter().map(|x| x + 5).collect();

        for input in inputs {
            let mut computer = IntcodeComputer::new(program.clone());
            computer.push_input(input);
            computers.get_mut().push(computer);
        }

        // execute all computers
        let mut last_out = 0;
        let mut finished = false;

        while !finished {
            for comp in computers.get_mut() {
                comp.push_input(last_out);

                match comp.exec() {
                    Some(IntcodeResult::Finished(output)) => {
                        finished = true;
                        last_out = output[0];
                    },
                    Some(IntcodeResult::WaitInput(output)) => {
                        last_out = output[0];
                    },
                    _ => ()
                }
            }
        }

        most = max(last_out, most);
    }

    println!("{}", most)
}
