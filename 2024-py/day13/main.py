import os.path
import re

from kryptikkaocutils.Timer import timer
from kryptikkaocutils.Input import write_input_to_file
from sympy import solve, Symbol


def play(ax, ay, bx, by, px, py, shift=False):
    a = Symbol("a", integer=True)
    b = Symbol("b", integer=True)
    if shift:
        px += 10000000000000
        py += 10000000000000
    roots = solve(
        [a * ax + b * bx - px, a * ay + b * by - py],
        [a, b],
    )
    if roots:
        return roots[a] * 3 + roots[b]
    else:
        return 0


@timer
def part1(inputs):
    s = 0
    for e in inputs:
        s += play(*e)
    print("Part1:", s)


@timer
def part2(inputs):
    s = 0
    for e in inputs:
        s += play(*e, True)
    print("Part2:", s)


if __name__ == "__main__":
    fname = "i.txt"
    if not os.path.isfile(fname):
        write_input_to_file(2024, 13, fname)
    inputs = [[int(num) for num in re.findall(r"\d+", machine)] for machine in (open(fname).read().split("\n\n"))]
    part1(inputs)
    part2(inputs)
