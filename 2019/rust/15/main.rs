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

#[derive(Debug, Clone)]
struct MazeDiscovery {
    computer : IntcodeComputer,
    grid : Vec<Vec<i64>>,
    distgrid : Vec<Vec<i64>>,
    x : i64,
    y : i64,
    dist : i64,
    oxygenx: i64,
    oxygeny: i64
}

impl MazeDiscovery {

    fn new(computer : IntcodeComputer) -> MazeDiscovery {
        let mut grid : Vec<Vec<i64>> = Vec::new();
        let mut dist : Vec<Vec<i64>> = Vec::new();
        for _ in 0..50 {
            grid.push(vec![-1 ; 50]);
            dist.push(vec![999999 ; 50]);
        }

        MazeDiscovery {
            computer: computer,
            grid: grid,
            distgrid: dist,
            x: 25,
            y: 25,
            dist: 0,
            oxygenx: 0,
            oxygeny: 0
        }
    }

    fn search(&mut self) {
        for i in 1..5 {
            self.mov(i);
        }
    }

    fn mov(&mut self, dir : i64) {
        let dirs : Vec<(i64, i64)> = vec![(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)];
        let dirinv : Vec<i64> = vec![0, 2, 1, 4, 3];

        let diru : usize = dir.try_into().unwrap();
        let dird = dirs[diru];
        let dy : usize = (self.y + dird.1).try_into().unwrap();
        let dx : usize = (self.x + dird.0).try_into().unwrap();

        // check if direction is already checked
        if self.grid[dy][dx] != -1 {
            return;
        }

        self.computer.push_input(dir);

        match self.computer.exec() {
            Some(IntcodeResult::WaitInput(output)) => {
                if output.is_empty() {
                    panic!("Got no output from intcode machine");
                }

                match output[0] {
                    0 => {
                        // wall
                        self.grid[dy][dx] = 0;
                    },
                    1 | 2 => {
                        // 1 = empty
                        self.grid[dy][dx] = output[0];

                        // move
                        self.y = self.y + dird.1;
                        self.x = self.x + dird.0;
                        self.dist = self.dist + 1;

                        if output[0] == 2 {
                            println!("Part one: {}", self.dist);
                            self.oxygenx = self.x;
                            self.oxygeny = self.y;
                        }

                        self.search();

                        // move back
                        self.computer.push_input(dirinv[diru]);
                        self.computer.exec();

                        self.y = self.y - dird.1;
                        self.x = self.x - dird.0;
                        self.dist = self.dist - 1;
                    },
                    _ => panic!("Wrong output from machine: {}", output[0])
                }
            },
            _ => panic!("Machine should never finish or fail")
        };
    }

    fn bfs(&self) -> i64 {
        let mut dist : Vec<Vec<i64>> = Vec::new();
        for _ in 0..50 {
            dist.push(vec![9999999 ; 50]);
        }

        let dirs : Vec<(i64, i64)> = vec![(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)];

        let x = self.oxygenx;
        let y = self.oxygeny;
        let tx : usize = x.try_into().unwrap();
        let ty : usize = y.try_into().unwrap();

        dist[ty][tx] = 0;

        let mut q = VecDeque::new();

        q.push_back((x, y));

        while !q.is_empty() {
            match q.pop_front() {
                Some((nx, ny)) => {
                    let tnx : usize = nx.try_into().unwrap();
                    let tny : usize = ny.try_into().unwrap();

                    match self.grid[tny][tnx] {
                        1 | 2 => {
                            for i in 1..5 {
                                let fx = nx + dirs[i].0;
                                let fy = ny + dirs[i].1;
                                let tfx : usize = fx.try_into().unwrap();
                                let tfy : usize = fy.try_into().unwrap();

                                if dist[tfy][tfx] > 1000 {
                                    q.push_back((fx, fy));
                                }
                                if dist[tny][tnx] + 1 < dist[tfy][tfx] {
                                    dist[tfy][tfx] = dist[tny][tnx] + 1;
                                }
                            }
                        },
                        _ => ()
                    }
                },
                _ => panic!("Really should not happen")
            }
        }

        let mut most = 0;
        for y in 0..50 {
            for x in 0..50 {
                if self.grid[y][x] == 1 || self.grid[y][x] == 2 {
                    most = max(most, dist[y][x]);
                }
            }
        }

        most
    }

    fn print(&self) {
        let mut printgrid = self.grid.clone();
        let cx : usize = self.x.try_into().unwrap();
        let cy : usize = self.y.try_into().unwrap();
        printgrid[cy][cx] = 7;

        for y in 0..50 {
            let mut outline = "".to_owned();
            for x in 0..50 {
                let pos = match printgrid[y][x] {
                    -1 => " ", // print . to show non-discovered areas
                    0  => "#",
                    1  => " ",
                    2  => "@",
                    7  => "D",
                    _  => "?"
                };
                outline.push_str(&pos[..]);
            }
            println!("{}", outline);
        }
    }
}

fn run(line : String) {
    let program: Vec<i64> = line.split(",")
                                  .map(|s| s.parse().unwrap())
                                  .collect();

    let mut maze = MazeDiscovery::new(IntcodeComputer::new(program));

    maze.search();
    println!("Part two: {}", maze.bfs());

    //maze.print();
}
