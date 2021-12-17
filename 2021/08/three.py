#!/usr/bin/env python3

from __future__ import annotations

DAY = 8
# https://adventofcode.com/2021/day/8

import argparse
import logging
import os


TEST_DATA = "sample"
REAL_DATA = "input"


def parse_args():
    parser = argparse.ArgumentParser(
        description=f"AdventOfCode: Day {DAY}")
    parser.set_defaults(
        input_filename=None,
        real=True,
        verbose=False,
        custom=False,
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--test", "-t", dest="real", action="store_false",
        help=f"Use {TEST_DATA!r} as input_filename")
    group.add_argument(
        "--real", "-r", dest="real", action="store_true",
        help="Use {REAL_DATA!r} as input_filename")

    parser.add_argument(
        "--custom", "-C", action="store_true",
        help="Use custom data")
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="More verbose logging")
    namespace = parser.parse_args()

    namespace.input_filename = REAL_DATA if namespace.real else TEST_DATA
    log_level = logging.DEBUG if namespace.verbose else logging.INFO
    logging.basicConfig(level=log_level)

    return namespace


def read_data(input_filename: str):
    with open(os.path.join(os.path.dirname(__file__), input_filename)) as f:
        return f.readlines()


# acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
def parse_data(text_data: str) -> list[int]:
    results = []
    for line in text_data:
        sigs, digs = line.split("|")
        signals = [s.strip() for s in sigs.split()]
        digits = [d.strip() for d in digs.split()]
        results.append((signals, digits))
    return results

#   0:      1:      2:      3:      4:
#  aaaa    ....    aaaa    aaaa    ....
# b    c  .    c  .    c  .    c  b    c
# b    c  .    c  .    c  .    c  b    c
#  ....    ....    dddd    dddd    dddd
# e    f  .    f  e    .  .    f  .    f
# e    f  .    f  e    .  .    f  .    f
#  gggg    ....    gggg    gggg    ....
# 
#   5:      6:      7:      8:      9:
#  aaaa    aaaa    aaaa    aaaa    aaaa
# b    .  b    .  .    c  b    c  b    c
# b    .  b    .  .    c  b    c  b    c
#  dddd    dddd    ....    dddd    dddd
# .    f  e    f  .    f  e    f  .    f
# .    f  e    f  .    f  e    f  .    f
#  gggg    gggg    ....    gggg    gggg

# counts
#  2:: 1: "cf"
#  3:: 7: "acf"
#  4:: 4: "bcdf"
#  5:: 2: "acdeg", 3: "acdfg", 5: "abdfg"
#  6:: 0: "abcefg", 6: "abdefg", 9:"abcdfg"
#  7:: 8: "abcdefg"

SEGMENTS = {       # count
    0: "abc.efg",  #     6
    1: "..c..f.",  # 2
    2: "a.cde.g",  #    5
    3: "a.cd.fg",  #    5
    4: ".bcd.f.",  #   4
    5: "ab.d.fg",  #    5
    6: "ab.defg",  #     6
    7: "a.c..f.",  #  3
    8: "abcdefg",  #      7
    9: "abcd.fg",  #     6
}

SEGMENT_SETS = {k: {c for c in v if c != '.'} for k, v in SEGMENTS.items()}
SEGMENT_DIGITS = {c: {k for k,v in SEGMENTS.items() if c in v} for c in "abcdefg"}

# a: 0.23.56789
# b: 0...456.89
# c: 01234..789
# d: ..23456.89
# e: 0.2...6.8.
# f: 01.3456789
# g: 0.23.56.89


def compute1(data) -> int:
    total = 0
    for _, digits in data:
        for d in digits:
            n = len(d)
            if n == 2:      # ..c..f.
                total += 1
            elif n == 3:    # a.c..f.
                total += 1
            elif n == 4:    # .bcd.f.
                total += 1
            elif n == 7:    # abcdefg
                total += 1
    return total


def compute2(data) -> int:
    total = 0
    for signals, digits in data:
        fives = []
        sixes = []
        one = four = seven = eight = None
        for s in signals:
            n = len(s)
            charset = {c for c in s}
            if n == 2:
                # 1: ..c..f.
                one = charset
            elif n == 3:
                # 7: a.c..f.
                seven = charset
            elif n == 4:
                # 4: .bcd.f.
                four = charset
            elif n == 5:
                # 2: a.cde.g
                # 3: a.cd.fg
                # 5: ab.d.fg
                fives.append(charset)
            elif n == 6:
                # 0: abc.efg
                # 6: ab.defg
                # 9: abcd.fg
                sixes.append(charset)
            elif n == 7:
                # 8: abcdefg
                eight = charset
        cf = one
        a = seven - cf
        bd = four - cf
        dg = (fives[0] & fives[1] & fives[2]) - a
        d = bd & dg
        b = bd - d
        g = dg - d
        bfg = (sixes[0] & sixes[1] & sixes[2]) - a
        f = cf & bfg
        c = cf - f
        e = eight - a - b - c - d - f - g
        tr = dict(a=a.pop(), b=b.pop(), c=c.pop(), d=d.pop(), e=e.pop(), f=f.pop(), g=g.pop())
        scrambled_digits = {str(d): {tr[seg] for seg in segs}
                            for d, segs in SEGMENT_SETS.items()}
        answer = []
        for d in digits:
            charset = {c for c in d}
            for d2, c2 in scrambled_digits.items():
                if charset == c2:
                    answer.append(d2)
                    break
        value = int("".join(answer), 10)
        total += value

    return total


def main():
    namespace = parse_args()
    if namespace.custom:
       data = parse_data(["acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"])
    else:
        text_data = read_data(namespace.input_filename)
        logging.info("%s", namespace.input_filename)
        logging.debug("%s", text_data)
        data = parse_data(text_data)
    logging.debug("\ndata: %s", data)
    result1 = compute1(data)
    print(f"{result1=}")
    result2 = compute2(data)
    print(f"{result2=}")


if __name__ == "__main__":
    raise SystemExit(main())
