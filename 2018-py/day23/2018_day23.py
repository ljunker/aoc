import time
import re
from heapq import heappop, heappush
from itertools import product

from aocfw import AdventOfCodeClient

YEAR = 2018
DAY = 23


def parse_bots(data):
    return [
        (tuple(numbers[:3]), numbers[3])
        for line in data.strip().splitlines()
        for numbers in [list(map(int, re.findall(r"-?\d+", line)))]
    ]


def distance_to_cube(point, corner, size):
    return sum(
        max(low - coordinate, coordinate - (low + size - 1), 0)
        for coordinate, low in zip(point, corner)
    )


def part1(part_data):
    bots = parse_bots(part_data)
    center, radius = max(bots, key=lambda bot: bot[1])
    return sum(distance_to_cube(point, center, 1) <= radius for point, _ in bots)


def part2(part_data):
    bots = parse_bots(part_data)
    corner = tuple(min(point[axis] - radius for point, radius in bots) for axis in range(3))
    span = max(
        point[axis] + radius - corner[axis] + 1
        for point, radius in bots
        for axis in range(3)
    )
    queue = []

    def enqueue(corner, size, candidates):
        intersecting = [
            (point, radius) for point, radius in candidates
            if distance_to_cube(point, corner, size) <= radius
        ]
        if intersecting:
            origin_distance = distance_to_cube((0, 0, 0), corner, size)
            heappush(queue, (-len(intersecting), origin_distance, size, corner, intersecting))

    enqueue(corner, 1 << (span - 1).bit_length(), bots)
    while queue:
        _, distance, size, corner, candidates = heappop(queue)
        # At a single point both priority bounds are exact.
        if size == 1:
            return distance
        half = size // 2
        for offsets in product((0, half), repeat=3):
            child = tuple(low + offset for low, offset in zip(corner, offsets))
            enqueue(child, half, candidates)


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

