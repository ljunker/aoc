import time

from aocfw import AdventOfCodeClient

YEAR = 2017
DAY = 24


def parse_components(part_data):
    return [tuple(map(int, line.split("/"))) for line in part_data.splitlines()]


def bridge_scores(components, port=0, used=None, strength=0, length=0):
    if used is None:
        used = set()

    best_strength = strength
    best_longest = (length, strength)

    for index, (left, right) in enumerate(components):
        if index in used or (left != port and right != port):
            continue

        used.add(index)
        next_port = right if left == port else left
        candidate_strength, candidate_longest = bridge_scores(
            components,
            next_port,
            used,
            strength + left + right,
            length + 1,
        )
        used.remove(index)

        best_strength = max(best_strength, candidate_strength)
        best_longest = max(best_longest, candidate_longest)

    return best_strength, best_longest


def part1(part_data):
    return bridge_scores(parse_components(part_data))[0]


def part2(part_data):
    return bridge_scores(parse_components(part_data))[1][1]


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
