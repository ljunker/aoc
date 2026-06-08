import time
import re
from collections import deque

from aocfw import AdventOfCodeClient

YEAR = 2018
DAY = 9


def parse_game(part_data):
    players, last_marble = map(int, re.findall(r"\d+", part_data))
    return players, last_marble


def high_score(players, last_marble):
    circle = deque([0])
    scores = [0] * players

    for marble in range(1, last_marble + 1):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[marble % players] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)

    return max(scores)


def part1(part_data):
    return high_score(*parse_game(part_data))


def part2(part_data):
    players, last_marble = parse_game(part_data)
    return high_score(players, last_marble * 100)


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
