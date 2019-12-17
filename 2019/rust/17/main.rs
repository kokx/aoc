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

fn run(line : String) {
    let program: Vec<i64> = line.split(",")
                                  .map(|s| s.parse().unwrap())
                                  .collect();

    let mut computer = IntcodeComputer::new(program.clone());

    let mut grid : Vec<Vec<char>> = Vec::new();

    match computer.exec() {
        Some(IntcodeResult::Finished(output)) | Some(IntcodeResult::WaitInput(output)) => {
            let mut line = Vec::new();

            for ic in output {
                let c : u32 = ic.try_into().unwrap();
                let c : char = c.try_into().unwrap();

                if c == '\n' {
                    grid.push(line);
                    line = Vec::new();
                } else {
                    line.push(c);
                }
            }
        },
        _ => panic!("Intcode Error")
    };

    let mut total = 0;

    for y in 0..grid.len() {
        for x in 0..grid[y].len() {
            print!("{}", grid[y][x]);

            // see if this is an intersection
            if grid[y][x] == '#' {
                let yi : i64 = y.try_into().unwrap();
                let xi : i64 = x.try_into().unwrap();

                let ym = yi - 1;
                let xm = xi - 1;

                //println!("Test0 {}-{}", x, y);

                if ym < 0 || xm < 0 {
                    continue;
                }
                let ym : usize = ym.try_into().unwrap();
                let xm : usize = xm.try_into().unwrap();

                //println!("Test1");

                let yp = yi + 1;
                let xp = xi + 1;

                if yp >= grid.len().try_into().unwrap() || xp >= grid[y].len().try_into().unwrap() {
                    continue;
                }
                let yp : usize = yp.try_into().unwrap();
                if xp >= grid[yp].len().try_into().unwrap() {
                    continue;
                }
                let xp : usize = xp.try_into().unwrap();

                //println!("Test");

                if grid[ym][x] == '#' && grid[yp][x] == '#' && grid[y][xm] == '#' && grid[y][xp] == '#' {
                    //println!("Test2");
                    total += yi * xi;
                }
            }
        }
        println!();
    }

    println!("{}", total);

    // part two
    let mut program = program;
    program[0] = 2;
    let program = program;

    /*
     * Path:
     *
     * R4,R10,R8,R4,R10,R6,R4,R4,R10,R8,R4,R10,R6,R4,R4,L12,R6,L12,R10,R6,R4,R4,L12,R6,L12,R4,R10,R8,R4,R10,R6,R4,R4,L12,R6,L12
     *
     * A: R4,R10,R8,R4,
     * B: R10,R6,R4,
     * A: R4,R10,R8,R4,
     * B: R10,R6,R4,
     * C: R4,L12,R6,L12,
     * B: R10,R6,R4,
     * C: R4,L12,R6,L12,
     * A: R4,R10,R8,R4,
     * B: R10,R6,R4,
     * C: R4,L12,R6,L12
     */

    let a = "R,4,R,10,R,8,R,4";
    let b = "R,10,R,6,R,4";
    let c = "R,4,L,12,R,6,L,12";

    let main_walk = "A,B,A,B,C,B,C,A,B,C";

    let mut computer = IntcodeComputer::new(program);

    let nl : u32 = '\n'.try_into().unwrap();
    let nl = nl.try_into().unwrap();

    for c in main_walk.chars() {
        let c : u32 = c.try_into().unwrap();
        computer.push_input(c.try_into().unwrap());
    }
    computer.push_input(nl);

    for c in a.chars() {
        let c : u32 = c.try_into().unwrap();
        computer.push_input(c.try_into().unwrap());
    }
    computer.push_input(nl);

    for c in b.chars() {
        let c : u32 = c.try_into().unwrap();
        computer.push_input(c.try_into().unwrap());
    }
    computer.push_input(nl);

    for c in c.chars() {
        let c : u32 = c.try_into().unwrap();
        computer.push_input(c.try_into().unwrap());
    }
    computer.push_input(nl);

    let n : u32 = 'n'.try_into().unwrap();
    let n = n.try_into().unwrap();
    computer.push_input(n);
    computer.push_input(nl);

    match computer.exec() {
        Some(IntcodeResult::Finished(output)) => {
            // print the last integer in the output, which is the answer
            let outputlast : i32 = output.len().try_into().unwrap();
            let outputlast : usize = (outputlast - 1).try_into().unwrap();
            let outputlast = output[outputlast];

            for ic in output {
                //println!("{}", ic);
                let c : u32 = ic.try_into().unwrap();
                let c : char = c.try_into().unwrap();

                print!("{}", c);
            }

            println!("Answer: {}", outputlast);
        },
        Some(IntcodeResult::WaitInput(output)) => {
            println!("Not finished {:?}", output);
        },
        _ => panic!("Something is wrong.")
    };

    // 1436 low
}
