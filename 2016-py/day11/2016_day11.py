import time
import re
from collections import deque
from itertools import combinations

from aocfw import AdventOfCodeClient

YEAR = 2016
DAY = 11

TOP_FLOOR = 3
FLOOR_ITEMS_RE = re.compile(r"(\w+)(?:-compatible microchip| generator)")


def parse_pairs(part_data):
    items = {}

    for floor, line in enumerate(part_data.splitlines()):
        for match in FLOOR_ITEMS_RE.finditer(line):
            item = match.group(0)
            element = match.group(1)
            chip_floor, generator_floor = items.get(element, (None, None))
            if item.endswith("microchip"):
                chip_floor = floor
            else:
                generator_floor = floor
            items[element] = (chip_floor, generator_floor)

    return tuple(sorted(items.values()))


def normalize(elevator, pairs):
    return elevator, tuple(sorted(pairs))


def is_valid(pairs):
    generator_floors = {generator for _, generator in pairs}
    return all(
        chip == generator or chip not in generator_floors
        for chip, generator in pairs
    )


def is_goal(pairs):
    return all(
        chip == TOP_FLOOR and generator == TOP_FLOOR
        for chip, generator in pairs
    )


def items_on_floor(pairs, floor):
    items = []
    for idx, (chip, generator) in enumerate(pairs):
        if chip == floor:
            items.append((idx, 0))
        if generator == floor:
            items.append((idx, 1))
    return items


def move_items(pairs, items, destination):
    moved = [list(pair) for pair in pairs]
    for idx, kind in items:
        moved[idx][kind] = destination
    return tuple(tuple(pair) for pair in moved)


def minimum_steps(part_data, extra_pairs=()):
    start_pairs = parse_pairs(part_data) + tuple(extra_pairs)
    start = normalize(0, start_pairs)
    queue = deque([(0, start)])
    seen = {start}

    while queue:
        steps, (elevator, pairs) = queue.popleft()
        if is_goal(pairs):
            return steps

        current_items = items_on_floor(pairs, elevator)
        below_has_items = any(
            chip < elevator or generator < elevator
            for chip, generator in pairs
        )

        for direction in (1, -1):
            destination = elevator + direction
            if destination < 0 or destination > TOP_FLOOR:
                continue
            if direction == -1 and not below_has_items:
                continue

            for move_size in (2, 1):
                for moving_items in combinations(current_items, move_size):
                    moved_pairs = move_items(pairs, moving_items, destination)
                    if not is_valid(moved_pairs):
                        continue

                    state = normalize(destination, moved_pairs)
                    if state in seen:
                        continue
                    seen.add(state)
                    queue.append((steps + 1, state))

    raise ValueError("No solution found")


def part1(part_data):
    return minimum_steps(part_data)


def part2(part_data):
    return minimum_steps(part_data, ((0, 0), (0, 0)))


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
