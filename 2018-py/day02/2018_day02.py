import time
from collections import Counter

from aocfw import AdventOfCodeClient

YEAR = 2018
DAY = 2


def box_ids(part_data):
    return part_data.splitlines()


def part1(part_data):
    twos = 0
    threes = 0

    for box_id in box_ids(part_data):
        counts = set(Counter(box_id).values())
        if 2 in counts:
            twos += 1
        if 3 in counts:
            threes += 1

    return twos * threes


def part2(part_data):
    ids = box_ids(part_data)

    for first_index, first in enumerate(ids):
        for second in ids[first_index + 1 :]:
            common = [left for left, right in zip(first, second) if left == right]
            if len(common) == len(first) - 1:
                return "".join(common)


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
