import time
import re

from aocfw import AdventOfCodeClient

YEAR = 2018
DAY = 10

FONT_ROWS = {
    "B": (
        "#####.",
        "#....#",
        "#....#",
        "#....#",
        "#####.",
        "#....#",
        "#....#",
        "#....#",
        "#....#",
        "#####.",
    ),
    "C": (
        ".####.",
        "#....#",
        "#.....",
        "#.....",
        "#.....",
        "#.....",
        "#.....",
        "#.....",
        "#....#",
        ".####.",
    ),
    "G": (
        ".####.",
        "#....#",
        "#.....",
        "#.....",
        "#.....",
        "#..###",
        "#....#",
        "#....#",
        "#...##",
        ".###.#",
    ),
    "H": (
        "#....#",
        "#....#",
        "#....#",
        "#....#",
        "######",
        "#....#",
        "#....#",
        "#....#",
        "#....#",
        "#....#",
    ),
    "J": (
        "...###",
        "....#.",
        "....#.",
        "....#.",
        "....#.",
        "....#.",
        "....#.",
        "#...#.",
        "#...#.",
        ".###..",
    ),
    "L": (
        "#.....",
        "#.....",
        "#.....",
        "#.....",
        "#.....",
        "#.....",
        "#.....",
        "#.....",
        "#.....",
        "######",
    ),
    "N": (
        "#....#",
        "##...#",
        "##...#",
        "#.#..#",
        "#.#..#",
        "#..#.#",
        "#..#.#",
        "#...##",
        "#...##",
        "#....#",
    ),
    "P": (
        "#####.",
        "#....#",
        "#....#",
        "#....#",
        "#####.",
        "#.....",
        "#.....",
        "#.....",
        "#.....",
        "#.....",
    ),
    "example_H": (
        "#...#",
        "#...#",
        "#...#",
        "#####",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
    ),
    "example_I": (
        "###",
        ".#.",
        ".#.",
        ".#.",
        ".#.",
        ".#.",
        ".#.",
        "###",
    ),
}
FONT = {
    "\n".join(rows): letter.removeprefix("example_")
    for letter, rows in FONT_ROWS.items()
}


def parse_points(part_data):
    return [tuple(map(int, re.findall(r"-?\d+", line))) for line in part_data.splitlines()]


def positions_at(points, seconds):
    return [
        (x + dx * seconds, y + dy * seconds)
        for x, y, dx, dy in points
    ]


def bounds(positions):
    xs = [x for x, _ in positions]
    ys = [y for _, y in positions]
    return min(xs), max(xs), min(ys), max(ys)


def area(positions):
    min_x, max_x, min_y, max_y = bounds(positions)
    return (max_x - min_x + 1) * (max_y - min_y + 1)


def find_message_time(part_data):
    points = parse_points(part_data)
    best_second = 0
    best_area = area(positions_at(points, 0))
    second = 1

    while True:
        current_area = area(positions_at(points, second))
        if current_area > best_area:
            return best_second

        best_second = second
        best_area = current_area
        second += 1


def render_message(part_data, seconds=None):
    if seconds is None:
        seconds = find_message_time(part_data)

    positions = set(positions_at(parse_points(part_data), seconds))
    min_x, max_x, min_y, max_y = bounds(positions)

    return "\n".join(
        "".join("#" if (x, y) in positions else "." for x in range(min_x, max_x + 1))
        for y in range(min_y, max_y + 1)
    )


def decode_message(message):
    rows = message.splitlines()
    has_pixel = [any(row[x] == "#" for row in rows) for x in range(len(rows[0]))]
    letters = []
    start = None

    for index, value in enumerate(has_pixel + [False]):
        if value and start is None:
            start = index
        elif not value and start is not None:
            block = "\n".join(row[start:index] for row in rows)
            letters.append(FONT.get(block, "?"))
            start = None

    return "".join(letters)


def part1(part_data):
    return decode_message(render_message(part_data))


def part2(part_data):
    return find_message_time(part_data)


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
