use std::io::{self, BufRead};
use std::convert::TryInto;
use std::collections::VecDeque;
//use std::collections::HashSet;
use std::cmp::max;

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

fn dfs(grid :Vec<Vec<i64>>, pos : (usize, usize)) -> Vec<i64> {
    // find series of directions to nearest empty (0) square
    let mut stack = Vec::new();
    let mut path = Vec::new();

    let px : i64 = pos.0.try_into().unwrap();
    let py : i64 = pos.1.try_into().unwrap();
    let pos = (px, py);

    let dirs : Vec<(i64, i64)> = vec![(0, 1), (0, -1), (1, 0), (-1, 0)];
    let dirsinv : Vec<(i64, i64)> = vec![(0, 0), (0, -1), (0, 1), (-1, 0), (1, 0)];
    let mut states = grid.clone();
    let mut prev = grid.clone();

    stack.push(pos);


    loop {
        match stack.pop() {
            Some(loc) => {
                let ty : usize = loc.1.try_into().unwrap();
                let tx : usize = loc.0.try_into().unwrap();
                states[ty][tx] = 20;
                match grid[ty][tx] {
                    0 => {
                        // unexplored, what we want to find
                        let mut prev_loc = loc;
                        while prev_loc != pos {
                            let py : usize = prev_loc.1.try_into().unwrap();
                            let px : usize = prev_loc.0.try_into().unwrap();
                            let mov = (prev[py][px] - 10) + 1;
                            path.push(mov);

                            let mov : usize = mov.try_into().unwrap();

                            let oy = prev_loc.1 + dirsinv[mov].1;
                            let ox = prev_loc.0 + dirsinv[mov].0;
                            prev_loc = (ox, oy);
                        }
                        break;
                    },
                    1 | 2 => {
                        // we can move here
                        for i in 0..4 {
                            let dir = dirs[i];
                            let oy = loc.1 + dir.1;
                            let dy : usize = oy.try_into().unwrap();
                            let ox = loc.0 + dir.0;
                            let dx : usize = ox.try_into().unwrap();

                            // already checked or in queue
                            if states[dy][dx] >= 10 {
                                continue;
                            }
                            stack.push((ox, oy));
                            states[dy][dx] = 10;
                            prev[dy][dx] = (10 + i).try_into().unwrap();
                        }
                    },
                    // nothing to see here, move along
                    5 => continue,
                    _ => continue
                }
            },
            None => break
        }
    }

    path.reverse();

    return path;
}

fn bfs(grid : Vec<Vec<i64>>, pos : (usize, usize)) -> i64 {
    let px : i64 = pos.0.try_into().unwrap();
    let py : i64 = pos.1.try_into().unwrap();
    let pos = (px, py);


    let mut states = grid.clone();
    let mut prev : Vec<Vec<i64>> = Vec::new();
    for _ in 0..grid.len() {
        let mut temp = Vec::new();
        for _ in 0..grid[0].len() {
            temp.push(99999999);
        }
        prev.push(temp);
    }

    let px : usize = pos.0.try_into().unwrap();
    let py : usize = pos.1.try_into().unwrap();

    let mut q = VecDeque::new();

    q.push_back(pos);
    prev[py][px] = 0;

    let dirs : Vec<(i64, i64)> = vec![(0, 1), (0, -1), (1, 0), (-1, 0)];

    loop {
        match q.pop_front() {
            Some(loc) => {
                let ty : usize = loc.1.try_into().unwrap();
                let tx : usize = loc.0.try_into().unwrap();
                states[ty][tx] = 20;
                match grid[ty][tx] {
                    1 => {
                        // we can move here
                        for i in 0..4 {
                            let dir = dirs[i];

                            let oy = loc.1 + dir.1;
                            let dy : usize = oy.try_into().unwrap();
                            let ox = loc.0 + dir.0;
                            let dx : usize = ox.try_into().unwrap();

                            if states[dy][dx] < 10 {
                                q.push_back((ox, oy));
                            }
                            states[dy][dx] = 10;
                            if prev[ty][tx] + 1 < prev[dy][dx] {
                                prev[dy][dx] = prev[ty][tx] + 1;
                            }
                        }
                    },
                    2 => {
                        return prev[ty][tx];
                    },
                    // cannot do anything here
                    5 => (),
                    _ => {
                        println!("Should not find this! {}", grid[ty][tx]);
                        break;
                    },
                }
            },
            None => break
        }
    }

    return 999999999;
}

fn bfs_fill(grid : Vec<Vec<i64>>, pos : (usize, usize)) -> i64 {
    let px : i64 = pos.0.try_into().unwrap();
    let py : i64 = pos.1.try_into().unwrap();
    let pos = (px, py);


    let mut states = grid.clone();
    let mut prev : Vec<Vec<i64>> = Vec::new();
    for _ in 0..grid.len() {
        let mut temp = Vec::new();
        for _ in 0..grid[0].len() {
            temp.push(99999999);
        }
        prev.push(temp);
    }

    let px : usize = pos.0.try_into().unwrap();
    let py : usize = pos.1.try_into().unwrap();

    let mut q = VecDeque::new();

    q.push_back(pos);
    prev[py][px] = 0;

    let dirs : Vec<(i64, i64)> = vec![(0, 1), (0, -1), (1, 0), (-1, 0)];

    loop {
        match q.pop_front() {
            Some(loc) => {
                let ty : usize = loc.1.try_into().unwrap();
                let tx : usize = loc.0.try_into().unwrap();
                states[ty][tx] = 20;
                match grid[ty][tx] {
                    1 | 2 => {
                        // we can move here
                        for i in 0..4 {
                            let dir = dirs[i];

                            let oy = loc.1 + dir.1;
                            let dy : usize = oy.try_into().unwrap();
                            let ox = loc.0 + dir.0;
                            let dx : usize = ox.try_into().unwrap();

                            if states[dy][dx] < 10 {
                                q.push_back((ox, oy));
                            }
                            states[dy][dx] = 10;
                            if prev[ty][tx] + 1 < prev[dy][dx] {
                                prev[dy][dx] = prev[ty][tx] + 1;
                            }
                        }
                    },
                    // cannot do anything here
                    5 => (),
                    _ => {
                        println!("Should not find this! {}", grid[ty][tx]);
                        break;
                    },
                }
            },
            None => break
        }
    }

    let mut most = 0;

    for i in 0..prev.len() {
        for j in 0..prev[0].len() {
            if prev[i][j] < 1000 {
                most = max(most, prev[i][j])
            }
        }
    }

    return most;
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

    let mut computer = IntcodeComputer::new(program);

    // initialize grid
    let mut grid : Vec<Vec<i64>> = Vec::new();
    for _ in 0..50 {
        let mut temp = Vec::new();
        for _ in 0..50 {
            temp.push(0);
        }
        grid.push(temp);
    }

    let mut cx = 25;
    let mut cy = 25;

    grid[cy][cx] = 1;

    // try to go top first
    let mut last_input = 1;
    computer.push_input(last_input);

    let mut q = VecDeque::new();

    let dirs : Vec<(i64, i64)> = vec![(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)];

    let mut found_loc = (0, 0);

    loop {
        let ty : i64 = cy.try_into().unwrap();
        let tx : i64 = cx.try_into().unwrap();
        match computer.exec() {
            Some(IntcodeResult::WaitInput(output)) => {
                if output.is_empty() {
                    println!("No output");
                }
                let last : usize = last_input.try_into().unwrap();
                let dir = dirs[last];
                let dy = ty + dir.1;
                let dy : usize = dy.try_into().unwrap();
                let dx = tx + dir.0;
                let dx : usize = dx.try_into().unwrap();

                match output[0] {
                    0 => {
                        // 5 = wall
                        grid[dy][dx] = 5;

                    },
                    1 => {
                        // 1 = empty
                        grid[dy][dx] = 1;

                        // move droid
                        cx = dx;
                        cy = dy;

                    },
                    2 => {
                        println!("Found it! ({}, {})", tx, ty);
                        grid[dy][dx] = 2;
                        found_loc = (dx, dy);

                        // move droid
                        cx = dx;
                        cy = dy;
                    },
                    _ => println!("Error! Wrong output!")
                };

                if q.is_empty() {
                    for m in dfs(grid.clone(), (cx, cy)) {
                        q.push_back(m);
                    }
                    if q.is_empty() {
                        break;
                    }
                }
                last_input = q.pop_front().unwrap();
                computer.push_input(last_input);
            },
            Some(IntcodeResult::Finished(output)) => {
                println!("fin: {:?}", output);
            },
            None => println!("Failed!")
        };
    }

    let dy : usize = cy.try_into().unwrap();
    let dx : usize = cx.try_into().unwrap();

    let mut printgrid = grid.clone();

    printgrid[dy][dx] = 7;

    // print grid
    for y in 0..50 {
        let mut outline = "".to_owned();
        for x in 0..50 {
            let pos = match printgrid[y][x] {
                0 => " ",
                1 => ".",
                2 => "@",
                5 => "#",
                7 => "D",
                _ => "?",
            };

            outline.push_str(&pos[..]);
        }
        println!("{}", outline);
    }

    println!("BFS: {}", bfs(grid.clone(), (25, 25)));
    // 351 high
    // apparently, off by one
    println!("BFS_fill: {}", bfs_fill(grid.clone(), found_loc) - 1);
}
