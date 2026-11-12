import time

from aocfw import AdventOfCodeClient

YEAR = 2018
DAY = 25


def part1(part_data):
    remaining = {
        tuple(map(int, line.split(","))) for line in part_data.splitlines()
    }
    constellations = 0
    while remaining:
        constellations += 1
        frontier = [remaining.pop()]
        while frontier:
            point = frontier.pop()
            neighbors = {
                other
                for other in remaining
                if sum(abs(a - b) for a, b in zip(point, other)) <= 3
            }
            remaining.difference_update(neighbors)
            frontier.extend(neighbors)
    return constellations


def part2(part_data):
    # Day 25 awards the final star once all other stars have been earned.
    return 0


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
