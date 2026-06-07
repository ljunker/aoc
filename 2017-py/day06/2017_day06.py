import time

from aocfw import AdventOfCodeClient

YEAR = 2017
DAY = 6


def parse_banks(part_data):
    return [int(value) for value in part_data.split()]


def redistribute(banks):
    index = max(range(len(banks)), key=lambda current: (banks[current], -current))
    blocks = banks[index]
    banks[index] = 0

    while blocks:
        index = (index + 1) % len(banks)
        banks[index] += 1
        blocks -= 1


def reallocation_cycles(part_data):
    banks = parse_banks(part_data)
    seen = {}
    cycles = 0

    while tuple(banks) not in seen:
        seen[tuple(banks)] = cycles
        redistribute(banks)
        cycles += 1

    return cycles, cycles - seen[tuple(banks)]


def part1(part_data):
    return reallocation_cycles(part_data)[0]


def part2(part_data):
    return reallocation_cycles(part_data)[1]


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
