import time
from collections import deque

from aocfw import AdventOfCodeClient

YEAR = 2016
DAY = 13


def is_open(x, y, favorite_number):
    if x < 0 or y < 0:
        return False

    value = x * x + 3 * x + 2 * x * y + y + y * y + favorite_number
    return value.bit_count() % 2 == 0


def neighbors(pos, favorite_number):
    x, y = pos
    candidates = (
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    )
    return [
        candidate
        for candidate in candidates
        if is_open(candidate[0], candidate[1], favorite_number)
    ]


def shortest_path(favorite_number, target):
    start = (1, 1)
    queue = deque([(0, start)])
    seen = {start}

    while queue:
        steps, pos = queue.popleft()
        if pos == target:
            return steps

        for neighbor in neighbors(pos, favorite_number):
            if neighbor in seen:
                continue
            seen.add(neighbor)
            queue.append((steps + 1, neighbor))

    raise ValueError(f"Target is unreachable: {target}")


def reachable_locations(favorite_number, max_steps):
    start = (1, 1)
    queue = deque([(0, start)])
    seen = {start}

    while queue:
        steps, pos = queue.popleft()
        if steps == max_steps:
            continue

        for neighbor in neighbors(pos, favorite_number):
            if neighbor in seen:
                continue
            seen.add(neighbor)
            queue.append((steps + 1, neighbor))

    return len(seen)


def part1(part_data):
    return shortest_path(int(part_data), (31, 39))


def part2(part_data):
    return reachable_locations(int(part_data), 50)


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
