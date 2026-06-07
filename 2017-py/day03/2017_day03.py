import time

from aocfw import AdventOfCodeClient

YEAR = 2017
DAY = 3


def spiral_positions():
    x = y = 0
    yield x, y

    step_length = 1
    while True:
        for dx, dy in ((1, 0), (0, 1)):
            for _ in range(step_length):
                x += dx
                y += dy
                yield x, y

        step_length += 1

        for dx, dy in ((-1, 0), (0, -1)):
            for _ in range(step_length):
                x += dx
                y += dy
                yield x, y

        step_length += 1


def distance_to_center(square):
    for value, position in enumerate(spiral_positions(), start=1):
        if value == square:
            x, y = position
            return abs(x) + abs(y)

    raise ValueError(f"Square not found: {square}")


def neighbor_positions(position):
    x, y = position
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx != 0 or dy != 0:
                yield x + dx, y + dy


def first_larger_value(limit):
    values = {}

    for position in spiral_positions():
        if position == (0, 0):
            value = 1
        else:
            value = sum(values.get(neighbor, 0) for neighbor in neighbor_positions(position))

        if value > limit:
            return value

        values[position] = value

    raise ValueError(f"No value found above {limit}")


def part1(part_data):
    return distance_to_center(int(part_data))


def part2(part_data):
    return first_larger_value(int(part_data))


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
