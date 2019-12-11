use std::io::{self, BufRead};
use std::convert::TryInto;
use std::collections::VecDeque;
use std::collections::HashSet;

// guess: 47780111 (too high)

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

    let mut cx : i64 = 1000;
    let mut cy : i64 = 1000;
    let mut dirx : i64 = 0;
    let mut diry : i64 = 1;

    let mut resultset = HashSet::new();

    loop {
        let ucx : usize = cx.try_into().unwrap();
        let ucy : usize = cy.try_into().unwrap();

        computer.push_input(grid[ucx][ucy]);

        match computer.exec() {
            Some(IntcodeResult::Finished(_output)) => {
                //println!("Finished: {:?}", output);
                break;
            },
            Some(IntcodeResult::WaitInput(output)) => {
                resultset.insert((cx, cy));

                // paint
                if output[0] == 1 {
                    grid[ucx][ucy] = 1;
                } else {
                    grid[ucx][ucy] = 0;
                }

                // turn robot
                if output[1] == 1 {
                    // turn right
                    if dirx == 0 && diry == 1 {
                        dirx = 1;
                        diry = 0;
                    } else if dirx == 0 && diry == -1 {
                        dirx = -1;
                        diry = 0;
                    } else if dirx == 1 && diry == 0 {
                        dirx = 0;
                        diry = -1;
                    } else if dirx == -1 && diry == 0 {
                        dirx = 0;
                        diry = 1;
                    }
                } else {
                    // turn left
                    if dirx == 0 && diry == 1 {
                        dirx = -1;
                        diry = 0;
                    } else if dirx == 0 && diry == -1 {
                        dirx = 1;
                        diry = 0;
                    } else if dirx == 1 && diry == 0 {
                        dirx = 0;
                        diry = 1;
                    } else if dirx == -1 && diry == 0 {
                        dirx = 0;
                        diry = -1;
                    }
                }

                // advance one
                cx = cx + dirx;
                cy = cy + diry;
            },
            None => println!("Failed or something")
        };
    }

    println!("{}", resultset.len());

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

    let mut cx : i64 = 1000;
    let mut cy : i64 = 1000;
    let mut dirx : i64 = 0;
    let mut diry : i64 = 1;

    let mut resultset = HashSet::new();

    grid[1000][1000] = 1;

    loop {
        let ucx : usize = cx.try_into().unwrap();
        let ucy : usize = cy.try_into().unwrap();

        computer.push_input(grid[ucx][ucy]);

        match computer.exec() {
            Some(IntcodeResult::Finished(_output)) => {
                //println!("Finished: {:?}", output);
                break;
            },
            Some(IntcodeResult::WaitInput(output)) => {
                resultset.insert((cx, cy));

                // paint
                if output[0] == 1 {
                    grid[ucx][ucy] = 1;
                } else {
                    grid[ucx][ucy] = 0;
                }

                // turn robot
                if output[1] == 1 {
                    // turn right
                    if dirx == 0 && diry == 1 {
                        dirx = 1;
                        diry = 0;
                    } else if dirx == 0 && diry == -1 {
                        dirx = -1;
                        diry = 0;
                    } else if dirx == 1 && diry == 0 {
                        dirx = 0;
                        diry = -1;
                    } else if dirx == -1 && diry == 0 {
                        dirx = 0;
                        diry = 1;
                    }
                } else {
                    // turn left
                    if dirx == 0 && diry == 1 {
                        dirx = -1;
                        diry = 0;
                    } else if dirx == 0 && diry == -1 {
                        dirx = 1;
                        diry = 0;
                    } else if dirx == 1 && diry == 0 {
                        dirx = 0;
                        diry = 1;
                    } else if dirx == -1 && diry == 0 {
                        dirx = 0;
                        diry = -1;
                    }
                }

                // advance one
                cx = cx + dirx;
                cy = cy + diry;
            },
            None => println!("Failed or something")
        };
    }

    for dy in 0..8 {
        let y = 1001 - dy;
        let mut str = "".to_owned();
        for x in 1000..1050 {
            if grid[x][y] == 1 {
                str.push_str("#");
            } else {
                str.push_str(" ");
            }
        }
        println!("{}", str);
    }
}
