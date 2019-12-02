use std::io::{self, BufRead};

fn main() {
    let stdin = io::stdin();

    for line in stdin.lock().lines() {
        run(line.unwrap());
    }
}

/// Execute an intcode program
///
/// # Arguments
///
/// * `program` - Vector of positive integers
/// * `noun` - Noun of the program, first argument of first operation
/// * `verb` - Verb of the program, second argument of first operation
///
/// # Remarks
///
/// Executes an intcode program as specified at:
/// - https://adventofcode.com/2019/day/2
///
fn exec(mut program : Vec<usize>, noun : usize, verb : usize) -> Option<usize> {
    let mut ic = 0;

    program[1] = noun;
    program[2] = verb;

    loop {
        let op = program[ic];

        // end of the program, do not read parameters
        if op == 99 {
            break;
        }

        // read all arguments of the op and verify if they do not create a crash
        let fir = program[ic+1];
        let sec = program[ic+2];
        let out = program[ic+3];

        if fir >= program.len() || sec >= program.len() || out >= program.len() {
            return None;
        }

        program[out] = match op {
            // +
            1 => program[fir] + program[sec],
            // *
            2 => program[fir] * program[sec],
            // do not change anything with a wrong opcode
            _ => program[out],
        };

        ic = ic + 4;
    }

    Some(program[0])
}

fn run(line : String) {
    let program: Vec<usize> = line.split(",")
                                  .map(|s| s.parse().unwrap())
                                  .collect();

    match exec(program.clone(), 12, 2) {
        Some(result) => println!("Part one: {}", result),
        _ => println!("Part one failed")
    }

    for noun in 0..100 {
        for verb in 0..100 {
            if let Some(result) = exec(program.clone(), noun, verb) {
                if  result == 19690720 {
                    println!("Part two: {}", noun * 100 + verb);
                }
            }
        }
    }
}
