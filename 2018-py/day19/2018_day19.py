import time
from math import isqrt
from pathlib import Path
from runpy import run_path

from aocfw import AdventOfCodeClient

YEAR = 2018
DAY = 19

apply_op = run_path(str(Path(__file__).resolve().parents[1] / "day16/2018_day16.py"))["apply_op"]


def execute(part_data, initial=0, stop_at=None):
    binding, *lines = part_data.strip().splitlines()
    bound_register = int(binding.split()[1])
    program = [(name, *map(int, operands)) for name, *operands in map(str.split, lines)]
    registers = [initial, 0, 0, 0, 0, 0]
    pointer = 0
    while 0 <= pointer < len(program) and pointer != stop_at:
        registers[bound_register] = pointer
        registers = apply_op(program[pointer][0], registers, *program[pointer][1:])
        pointer = registers[bound_register] + 1
    return registers


def part1(part_data):
    return execute(part_data)[0]


def part2(part_data):
    # Instruction 1 starts the input's nested divisor loop.
    registers = execute(part_data, initial=1, stop_at=1)
    target = registers[5]
    total = registers[0]
    for divisor in range(1, isqrt(target) + 1):
        quotient, remainder = divmod(target, divisor)
        if remainder == 0:
            total += divisor
            if quotient != divisor:
                total += quotient
    return total


if __name__ == "__main__":
    client = AdventOfCodeClient()

    data = client.get_input(YEAR, DAY)
    answer = part1(data)
    print("Part 1:", answer)
    res = client.submit_answer(YEAR, DAY, 1, answer)
    print(res.message)

    time.sleep(10)

    answer = part2(data)
    print("Part 2:", answer)
    res = client.submit_answer(YEAR, DAY, 2, answer)
    print(res.message)

