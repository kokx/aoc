use std::io::{self, BufRead};
use std::convert::TryInto;
use std::collections::VecDeque;
use std::collections::HashSet;
use std::cmp::{min, max};

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

#[derive(Debug)]
struct IntcodeComputer {
    program : Vec<i64>,
    input : VecDeque<i64>,
    ic : usize,
    relative_base : i64
}

impl IntcodeComputer {

    fn new(prog : Vec<i64>) -> IntcodeComputer {
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

    // increase program size
    let mut program = program;
    for _ in 0..10000 {
        program.push(0);
    }

    // no need to modify the program again
    let program = program;

    println!("Part one:");
    println!("---------");

    let mut computer = IntcodeComputer::new(program.clone());

    // initialize grid
    let mut grid : Vec<Vec<i64>> = Vec::new();
    for _ in 0..2000 {
        let mut temp = Vec::new();
        for _ in 0..2000 {
            temp.push(0);
        }
        grid.push(temp);
    }

    let mut cx : usize = 1000;
    let mut cy : usize = 1000;

    let mut leastx = 2000;
    let mut mostx = 0;
    let mut leasty = 2000;
    let mut mosty = 0;

    match computer.exec() {
        Some(IntcodeResult::Finished(output)) => {
            //println!("{:?}", output)
            let mut num : i64 = 0;

            for o in output {
                if num % 3 == 0 {
                    let tempx = 1000 + o;
                    cx = tempx.try_into().unwrap();
                }
                if num % 3 == 1 {
                    let tempy = 1000 + o;
                    cy = tempy.try_into().unwrap();
                }
                if num % 3 == 2 {
                    grid[cy][cx] = o;
                    leastx = min(cx, leastx);
                    leasty = min(cy, leasty);
                    mostx = max(cx, mostx);
                    mosty = max(cy, mosty);
                }

                num += 1;
            }
        },
        Some(IntcodeResult::WaitInput(output)) => println!("Wait: {:?}", output),
        None => println!("None")
    }

    let mut blocks = 0;

    println!("x: ({}, {}), y: ({}, {})", leastx, mostx, leasty, mosty);

    leasty -= 2;
    mosty += 2;
    leastx -= 2;
    mostx += 2;

    for y in leasty..mosty {
        let mut outline = "".to_owned();
        for x in leastx..mostx {
            if grid[y][x] == 2 {
                blocks += 1
            }
            let pos = grid[y][x].to_string();
            outline.push_str(&pos[..]);
        }
        println!("{}", outline);
    }

    // 41 wrong
    println!("{}", blocks);

    let mut program = program;

    // insert coin!
    program[0] = 2;

    println!("Part two:");
    println!("---------");

    let mut computer = IntcodeComputer::new(program.clone());

    // initialize grid
    let mut grid : Vec<Vec<i64>> = Vec::new();
    for _ in 0..2000 {
        let mut temp = Vec::new();
        for _ in 0..2000 {
            temp.push(0);
        }
        grid.push(temp);
    }

    let mut cx : usize = 1000;
    let mut cy : usize = 1000;

    let mut leastx = 2000;
    let mut mostx = 0;
    let mut leasty = 2000;
    let mut mosty = 0;

    let mut last_score = 0;

    for _ in 0..7300 {

        match computer.exec() {
            Some(IntcodeResult::Finished(output)) => {
                //println!("{:?}", output)
                let mut num : i64 = 0;

                for o in output {
                    if num % 3 == 0 {
                        let tempx = 1000 + o;
                        cx = tempx.try_into().unwrap();
                    }
                    if num % 3 == 1 {
                        let tempy = 1000 + o;
                        cy = tempy.try_into().unwrap();
                    }
                    if num % 3 == 2 {
                        if cx == 999 && cy == 1000 {
                            println!("Score: {}", o);
                            last_score = o;
                        } else {
                            grid[cy][cx] = o;
                            leastx = min(cx, leastx);
                            leasty = min(cy, leasty);
                            mostx = max(cx, mostx);
                            mosty = max(cy, mosty);
                        }
                    }

                    num += 1;
                }
            },
            Some(IntcodeResult::WaitInput(output)) => {
                println!("{:?}", output);
                let mut num : i64 = 0;

                for o in output {
                    if num % 3 == 0 {
                        let tempx = 1000 + o;
                        cx = tempx.try_into().unwrap();
                    }
                    if num % 3 == 1 {
                        let tempy = 1000 + o;
                        cy = tempy.try_into().unwrap();
                    }
                    if num % 3 == 2 {
                        if cx == 999 && cy == 1000 {
                            println!("Score: {}", o);
                            last_score = o;
                        } else {
                            grid[cy][cx] = o;
                            leastx = min(cx, leastx);
                            leasty = min(cy, leasty);
                            mostx = max(cx, mostx);
                            mosty = max(cy, mosty);
                        }
                    }

                    num += 1;
                }
            },
            None => println!("None")
        }

        let mut blocks = 0;

        //println!("x: ({}, {}), y: ({}, {})", leastx, mostx, leasty, mosty);
        if leastx == 2000 {
            break;
        }

        let miny = leasty - 2;
        let maxy = mosty + 2;
        let minx = leastx - 2;
        let maxx = mostx + 2;

        let mut ballx = 0;
        let mut paddlex = 0;

        for y in miny..maxy {
            let mut outline = "".to_owned();
            for x in minx..maxx {
                if grid[y][x] == 2 {
                    blocks += 1
                }
                let pos = match grid[y][x] {
                    0 => " ",
                    1 => "#",
                    2 => "x",
                    3 => "_",
                    4 => "*",
                    _ => "?",
                };

                if grid[y][x] == 4 {
                    ballx = x;
                }
                if grid[y][x] == 3 {
                    paddlex = x;
                }

                outline.push_str(&pos[..]);
            }
            println!("{}", outline);
        }

        if paddlex > ballx {
            computer.push_input(-1);
        } else if paddlex < ballx {
            computer.push_input(1);
        } else {
            computer.push_input(0);
        }
    }

    // 41 wrong
    // 11983 low
    println!("score: {}", last_score);
}
