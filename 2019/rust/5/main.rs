use std::io::{self, BufRead};
use std::convert::TryInto;
use std::collections::VecDeque;

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

/// Execute an intcode program
///
/// # Arguments
///
/// * `program` - Vector of integers
/// * `input` - Vector of input values, read from front to back
///
/// # Remarks
///
/// Executes an intcode program as specified at:
/// - https://adventofcode.com/2019/day/5
///
fn exec(mut program : Vec<i32>, input : Vec<i32>) -> Option<i32> {
    let mut ic = 0;

    let mut input : VecDeque<i32> = input.try_into().unwrap();

    loop {
        // split the op into op and mode else
        let modes = program[ic] / 100;
        let op = program[ic] % 100;

        match op {
            // end of the program
            99 => break,
            3 | 4 => {
                // input and output, with one parameter

                match op {
                    3 => {
                        let a : usize = program[ic+1].try_into().unwrap();
                        program[a] = input.pop_front()?;
                    },
                    4 => {
                        let a = get_param(&program, mode(modes, 0), ic+1)?;
                        println!("{}", a);
                    },
                    _ => ()
                }

                if op == 3 {
                } else if op == 4 {
                    // read 1 parameter and output its value

                }
                ic = ic + 2;
            },
            5 | 6 => {
                // conditional jumps, with two parameters
                let a = get_param(&program, mode(modes, 0), ic+1)?;
                let b = get_param(&program, mode(modes, 1), ic+2)?;

                // 5: jump if not zero
                // 6: jump if zero
                if (a == 0 && op == 6) || (a != 0 && op == 5) {
                    ic = b.try_into().unwrap();
                } else {
                    ic += 3;
                }
            },
            1 | 2 | 7 | 8 => {
                // with three parameters
                let a = get_param(&program, mode(modes, 0), ic+1)?;
                let b = get_param(&program, mode(modes, 1), ic+2)?;

                let out : usize = program[ic+3].try_into().unwrap();

                if out >= program.len() {
                    return None;
                }

                program[out] = match op {
                    // +
                    1 => a + b,
                    // *
                    2 => a * b,
                    // <
                    7 => (a < b).try_into().unwrap(),
                    // ==
                    8 => (a == b).try_into().unwrap(),
                    // all otehr cases, just return c
                    _ => program[out]
                };


                ic = ic + 4;
            },
            _ => {
                println!("Unkown instruction: {}", op);
                return None;
            }
        }
    }

    Some(0)
}

fn run(line : String) {
    let program: Vec<i32> = line.split(",")
                                  .map(|s| s.parse().unwrap())
                                  .collect();

    println!("Part one:");
    println!("---------");
    if exec(program.clone(), vec![1]) == None {
        println!("Part one failed!");
    }

    println!();

    println!("Part two:");
    println!("---------");
    if exec(program.clone(), vec![5]) == None {
        println!("Part two failed!");
    }
}
