import time
from itertools import cycle

from aocfw import AdventOfCodeClient

YEAR = 2018
DAY = 1


def parse_changes(part_data):
    return [int(line) for line in part_data.splitlines()]


def part1(part_data):
    return sum(parse_changes(part_data))


def part2(part_data):
    frequency = 0
    seen = {frequency}

    for change in cycle(parse_changes(part_data)):
        frequency += change
        if frequency in seen:
            return frequency

        seen.add(frequency)


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
