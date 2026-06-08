import time
from collections import defaultdict
from math import isqrt

from aocfw import AdventOfCodeClient

YEAR = 2017
DAY = 23


def parse_instructions(part_data):
    return [line.split() for line in part_data.splitlines()]


def value(registers, token):
    try:
        return int(token)
    except ValueError:
        return registers[token]


def run_program(instructions, initial_registers=None):
    registers = defaultdict(int)
    if initial_registers is not None:
        registers.update(initial_registers)

    index = 0
    mul_count = 0

    while 0 <= index < len(instructions):
        operation, x, y = instructions[index]

        if operation == "set":
            registers[x] = value(registers, y)
        elif operation == "sub":
            registers[x] -= value(registers, y)
        elif operation == "mul":
            registers[x] *= value(registers, y)
            mul_count += 1
        elif operation == "jnz" and value(registers, x) != 0:
            index += value(registers, y)
            continue

        index += 1

    return registers, mul_count


def part2_bounds(instructions):
    start = None
    end = None

    for operation, x, y in instructions[:8]:
        if operation == "set" and x == "b":
            start = int(y)
        elif operation == "mul" and x == "b":
            start *= int(y)
        elif operation == "sub" and x == "b":
            start -= int(y)
        elif operation == "set" and x == "c" and y == "b":
            end = start
        elif operation == "sub" and x == "c":
            end -= int(y)

    step = -int([instruction[2] for instruction in instructions if instruction[:2] == ["sub", "b"]][-1])
    return start, end, step


def is_composite(number):
    if number < 4:
        return False
    if number % 2 == 0:
        return True

    for divisor in range(3, isqrt(number) + 1, 2):
        if number % divisor == 0:
            return True

    return False


def part1(part_data):
    return run_program(parse_instructions(part_data))[1]


def part2(part_data):
    start, end, step = part2_bounds(parse_instructions(part_data))
    return sum(is_composite(number) for number in range(start, end + 1, step))


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
