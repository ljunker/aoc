import time
import hashlib
from collections import deque

from aocfw import AdventOfCodeClient

YEAR = 2016
DAY = 17

DIRECTIONS = (
    ("U", 0, -1),
    ("D", 0, 1),
    ("L", -1, 0),
    ("R", 1, 0),
)
OPEN_DOORS = set("bcdef")


def open_doors(passcode, path):
    hash_value = hashlib.md5(f"{passcode}{path}".encode()).hexdigest()
    return [
        direction
        for direction, is_open in zip(DIRECTIONS, hash_value[:4])
        if is_open in OPEN_DOORS
    ]


def next_states(passcode, x, y, path):
    for direction, dx, dy in open_doors(passcode, path):
        nx = x + dx
        ny = y + dy
        if 0 <= nx < 4 and 0 <= ny < 4:
            yield nx, ny, path + direction


def find_paths(passcode):
    queue = deque([(0, 0, "")])
    shortest = None
    longest = 0

    while queue:
        x, y, path = queue.popleft()

        if (x, y) == (3, 3):
            if shortest is None:
                shortest = path
            longest = max(longest, len(path))
            continue

        queue.extend(next_states(passcode, x, y, path))

    return shortest, longest


def part1(part_data):
    shortest, _ = find_paths(part_data.strip())
    return shortest


def part2(part_data):
    _, longest = find_paths(part_data.strip())
    return longest


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
