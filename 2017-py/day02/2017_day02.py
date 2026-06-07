import time
from itertools import permutations

from aocfw import AdventOfCodeClient

YEAR = 2017
DAY = 2


def parse_rows(part_data):
    return [
        [int(value) for value in line.split()]
        for line in part_data.splitlines()
        if line.strip()
    ]


def divisible_result(row):
    for left, right in permutations(row, 2):
        if left % right == 0:
            return left // right

    raise ValueError(f"No divisible pair found in row: {row}")


def part1(part_data):
    return sum(max(row) - min(row) for row in parse_rows(part_data))


def part2(part_data):
    return sum(divisible_result(row) for row in parse_rows(part_data))


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
