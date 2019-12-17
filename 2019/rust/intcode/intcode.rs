use std::io::{self, BufRead, BufReader};
use std::convert::TryInto;
use std::collections::VecDeque;
//use std::collections::HashSet;
//use std::cmp::max;
use std::env;
use std::fs::{self, File};
use std::process::exit;

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

fn print_output(output : Vec<i64>) {
    for c in output {
        if c > 128 {
            println!("intcode: Non ASCII output: {}", c);
        } else {
            let c : u32 = c.try_into().unwrap();
            let c : char = c.try_into().unwrap();
            print!("{}", c);
        }
    }
}

fn read_program(path : String) -> Vec<i64> {

    let reader = BufReader::new(File::open(path).unwrap());
    let mut program = "".to_owned();

    for line in reader.lines() {
        let line = line.expect("Error when reading Intcode program");
        program.push_str(&line);
    }

    return program.split(",")
                  .map(|s| s.parse().unwrap())
                  .collect();
}

fn read_input() -> Vec<i64> {
    let mut input_text = String::new();
    io::stdin()
        .read_line(&mut input_text)
        .expect("Problem reading input.");

    let mut input_vec = Vec::new();

    for c in input_text.chars() {
        let c : u32 = c.try_into().unwrap();
        input_vec.push(c.try_into().unwrap());
    }

    return input_vec;
}

fn run(program : Vec<i64>) {
    let mut computer = IntcodeComputer::new(program);

    loop {
        match computer.exec() {
            Some(IntcodeResult::Finished(output)) => print_output(output),
            Some(IntcodeResult::WaitInput(output)) => {
                print_output(output);

                for val in read_input() {
                    computer.push_input(val);
                }

                // only case where we continue execution
                continue;
            },
            None => {
                println!("Error in intcode program execution.");
                exit(2);
            }
        };
        // by default, stop execution
        break;
    }
}

fn main() {
    let mut path = "".to_owned();

    let mut changes = Vec::new();

    let mut args : VecDeque<String> = env::args().collect();
    // pop the first argument (program name)
    args.pop_front();

    for arg in args {
        if arg.len() >= 3 && &arg[0..2] == "-c" {
            let split : Vec<i64> = arg[2..].split("=").map(|s| s.parse().unwrap()).collect();

            changes.push((split[0], split[1]));
        } else {
            path = arg.to_owned();
        }
    }

    if !fs::metadata(&path).is_ok() {
        println!("Input file '{}' could not be found.", path);
        exit(1);
    }

    let mut program = read_program(path);

    // apply program changes
    for (index, value) in changes {
        let index : usize = index.try_into().unwrap();

        program[index] = value;
    }

    run(program);
}
