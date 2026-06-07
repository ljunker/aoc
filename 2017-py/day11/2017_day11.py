import time

from aocfw import AdventOfCodeClient

YEAR = 2017
DAY = 11

DIRECTIONS = {
    "n": (0, 1, -1),
    "ne": (1, 0, -1),
    "se": (1, -1, 0),
    "s": (0, -1, 1),
    "sw": (-1, 0, 1),
    "nw": (-1, 1, 0),
}


def distance(position):
    return max(abs(coordinate) for coordinate in position)


def walk(part_data):
    position = (0, 0, 0)
    furthest = 0

    for step in part_data.strip().split(","):
        dx, dy, dz = DIRECTIONS[step]
        x, y, z = position
        position = (x + dx, y + dy, z + dz)
        furthest = max(furthest, distance(position))

    return distance(position), furthest


def part1(part_data):
    return walk(part_data)[0]


def part2(part_data):
    return walk(part_data)[1]


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
