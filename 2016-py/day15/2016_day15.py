import time
import math
import re

from aocfw import AdventOfCodeClient

YEAR = 2016
DAY = 15


def parse_discs(part_data):
    discs = []
    for line in part_data.splitlines():
        match = re.fullmatch(
            r"Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).",
            line,
        )
        if not match:
            raise ValueError(f"Cannot parse disc: {line}")
        disc, positions, start = map(int, match.groups())
        discs.append((disc, positions, start))
    return discs


def first_drop_time(discs):
    drop_time = 0
    step = 1

    for disc, positions, start in discs:
        while (start + drop_time + disc) % positions != 0:
            drop_time += step
        step = math.lcm(step, positions)

    return drop_time


def part1(part_data):
    return first_drop_time(parse_discs(part_data))


def part2(part_data):
    discs = parse_discs(part_data)
    discs.append((len(discs) + 1, 11, 0))
    return first_drop_time(discs)


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
