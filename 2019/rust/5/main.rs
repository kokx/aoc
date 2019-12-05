use std::io::{self, BufRead};
use std::convert::TryInto;

// guess: 47780111 (too high)

fn main() {
    let stdin = io::stdin();

    for line in stdin.lock().lines() {
        run(line.unwrap());
    }
}

fn get_param_value(program : &Vec<i32>, mode : i32, loc : usize) -> Option<i32> {
    let mode = mode % 10;
    if mode == 1 {
        return Some(program[loc]);
    }

    let pos : usize = program[loc].try_into().unwrap();
    if pos > program.len() {
        return None;
    }
    return Some(program[pos]);
}

/// Execute an intcode program
///
/// # Arguments
///
/// * `program` - Vector of positive integers
///
/// # Remarks
///
/// Executes an intcode program as specified at:
/// - https://adventofcode.com/2019/day/5
///
fn exec(mut program : Vec<i32>) -> Option<i32> {
    let mut ic = 0;

    loop {
        // split the op into op and mode else
        let modes = program[ic] / 100;
        let op = program[ic] % 100;

        // end of the program, do not read parameters
        if op == 99 {
            //println!("{}", program[ic]);
            break;
        } else if op == 1 || op == 2 || op == 7 || op == 8 {
            //println!("{} => ({} {}) {} {} {}", program[ic], modes, op, program[ic+1], program[ic+2], program[ic+3]);
            // read 3 parameters
            let fir = get_param_value(&program, modes / 1, ic+1)?;
            let sec = get_param_value(&program, modes / 10, ic+2)?;

            let out : usize = program[ic+3].try_into().unwrap();

            if out >= program.len() {
                return None;
            }

            program[out] = match op {
                // +
                1 => fir + sec,
                // *
                2 => fir * sec,
                // <
                7 => (fir < sec).try_into().unwrap(),
                // ==
                8 => (fir == sec).try_into().unwrap(),
                // do not change anything with a wrong opcode
                _ => program[out],
            };

            //println!("-> {}", program[out]);

            ic = ic + 4;
        } else if op == 3 || op == 4 {
            println!("{} => {} {}", program[ic], op, program[ic+1]);
            if op == 3 {
                let fir : usize = program[ic+1].try_into().unwrap();
                // TODO: write actual input
                program[fir] = 5;
                println!("Writing to {}", fir);
            } else if op == 4 {
                // read 1 parameter and output its value
                let fir = get_param_value(&program, modes / 1, ic+1)?;
                println!("out: {}", fir);
                println!("---------------------");

            }
            ic = ic + 2;
        } else if op == 5 || op == 6 {
            let fir = get_param_value(&program, modes / 1, ic+1)?;
            let sec = get_param_value(&program, modes / 10, ic+2)?;

            // 5: jump if not zero
            // 6: jump if zero

            if (fir == 0 && op == 6) || (fir != 0 && op == 5) {
                ic = sec.try_into().unwrap();
            } else {
                ic += 3;
            }
        } else {
            println!("Unknown instruction: {}", op);
        }
    }

    Some(0)
}

fn run(line : String) {
    let program: Vec<i32> = line.split(",")
                                  .map(|s| s.parse().unwrap())
                                  .collect();

    match exec(program.clone()) {
        Some(result) => println!("Part one: {}", result),
        _ => println!("Part one failed")
    }
}
