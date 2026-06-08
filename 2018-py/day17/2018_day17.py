import time
import re

from aocfw import AdventOfCodeClient

YEAR = 2018
DAY = 17


def part1(part_data):
    flowing, settled, _, min_y, max_y = simulate_water(part_data)
    return sum(
        1
        for _, y in flowing | settled
        if min_y <= y <= max_y
    )


def part2(part_data):
    _, settled, _, min_y, max_y = simulate_water(part_data)
    return sum(
        1
        for _, y in settled
        if min_y <= y <= max_y
    )


def parse_clay(part_data):
    clay = set()

    for line in part_data.splitlines():
        fixed_axis, fixed_value, range_axis, start, end = re.match(
            r"([xy])=(\d+), ([xy])=(\d+)\.\.(\d+)",
            line,
        ).groups()
        fixed_value = int(fixed_value)
        start = int(start)
        end = int(end)

        for value in range(start, end + 1):
            if fixed_axis == "x":
                clay.add((fixed_value, value))
            else:
                clay.add((value, fixed_value))

    min_y = min(y for _, y in clay)
    max_y = max(y for _, y in clay)
    min_x = min(x for x, _ in clay) - 1
    max_x = max(x for x, _ in clay) + 1
    return clay, min_x, max_x, min_y, max_y


def simulate_water(part_data):
    clay, min_x, max_x, min_y, max_y = parse_clay(part_data)
    flowing = set()
    settled = set()
    sources = [(500, 0)]
    seen_sources = {(500, 0)}

    def blocked(position):
        return position in clay or position in settled

    def scan_side(x, y, dx):
        while True:
            next_x = x + dx
            if next_x < min_x or next_x > max_x:
                return next_x, False
            if (next_x, y) in clay:
                return x, True
            if not blocked((next_x, y + 1)):
                return next_x, False
            x = next_x

    while sources:
        x, y = sources.pop()

        while y <= max_y and not blocked((x, y + 1)):
            flowing.add((x, y))
            y += 1

        if y > max_y:
            continue

        while y >= 0:
            left, left_wall = scan_side(x, y, -1)
            right, right_wall = scan_side(x, y, 1)

            for current_x in range(left, right + 1):
                flowing.add((current_x, y))

            if left_wall and right_wall:
                for current_x in range(left, right + 1):
                    settled.add((current_x, y))
                y -= 1
                continue

            if not left_wall:
                flowing.add((left, y))
                if (left, y) not in seen_sources:
                    seen_sources.add((left, y))
                    sources.append((left, y))
            if not right_wall:
                flowing.add((right, y))
                if (right, y) not in seen_sources:
                    seen_sources.add((right, y))
                    sources.append((right, y))
            break

    return flowing, settled, clay, min_y, max_y


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
