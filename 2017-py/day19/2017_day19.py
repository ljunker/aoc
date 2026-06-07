import time

from aocfw import AdventOfCodeClient

YEAR = 2017
DAY = 19


DIRECTIONS = {
    "down": (0, 1),
    "up": (0, -1),
    "left": (-1, 0),
    "right": (1, 0),
}


def trace_route(part_data):
    lines = part_data.splitlines()
    width = max(len(line) for line in lines)
    grid = [line.ljust(width) for line in lines]
    x = grid[0].index("|")
    y = 0
    dx, dy = DIRECTIONS["down"]
    letters = []
    steps = 0

    while 0 <= y < len(grid) and 0 <= x < width and grid[y][x] != " ":
        value = grid[y][x]
        steps += 1

        if value.isalpha():
            letters.append(value)
        elif value == "+":
            for next_dx, next_dy in DIRECTIONS.values():
                if (next_dx, next_dy) == (-dx, -dy):
                    continue

                next_x = x + next_dx
                next_y = y + next_dy
                if (
                    0 <= next_y < len(grid)
                    and 0 <= next_x < width
                    and grid[next_y][next_x] != " "
                ):
                    dx, dy = next_dx, next_dy
                    break

        x += dx
        y += dy

    return "".join(letters), steps


def part1(part_data):
    return trace_route(part_data)[0]


def part2(part_data):
    return trace_route(part_data)[1]


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
