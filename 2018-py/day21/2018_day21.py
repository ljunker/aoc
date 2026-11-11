import time

from aocfw import AdventOfCodeClient

YEAR = 2018
DAY = 21


def halt_values(part_data):
    # Translate the loop at instructions 6-27. Instruction 28 compares
    # each generated value with register 0.
    _, *program = [line.split() for line in part_data.strip().splitlines()]
    high_bit = int(program[6][2])
    seed = int(program[7][1])
    low_mask = int(program[8][2])
    value_mask = int(program[10][2])
    multiplier = int(program[11][2])
    base = int(program[13][1])

    value = 0
    while True:
        remaining = value | high_bit
        value = seed
        while True:
            value = (value + (remaining & low_mask)) & value_mask
            value = (value * multiplier) & value_mask
            if remaining < base:
                break
            remaining //= base
        yield value


def part1(part_data):
    return next(halt_values(part_data))


def part2(part_data):
    seen = set()
    previous = None
    for value in halt_values(part_data):
        if value in seen:
            return previous
        seen.add(value)
        previous = value


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

