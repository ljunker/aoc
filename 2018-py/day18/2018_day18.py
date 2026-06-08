import time

from aocfw import AdventOfCodeClient

YEAR = 2018
DAY = 18


def part1(part_data):
    return resource_value_after(part_data, 10)


def part2(part_data):
    return resource_value_after(part_data, 1_000_000_000)


def parse_grid(part_data):
    return tuple(part_data.strip().splitlines())


def adjacent_acres(grid, x, y):
    height = len(grid)
    width = len(grid[0])

    for next_y in range(max(0, y - 1), min(height, y + 2)):
        for next_x in range(max(0, x - 1), min(width, x + 2)):
            if next_x != x or next_y != y:
                yield grid[next_y][next_x]


def step(grid):
    rows = []

    for y, row in enumerate(grid):
        next_row = []

        for x, acre in enumerate(row):
            adjacent = list(adjacent_acres(grid, x, y))
            trees = adjacent.count("|")
            lumberyards = adjacent.count("#")

            if acre == "." and trees >= 3:
                next_row.append("|")
            elif acre == "|" and lumberyards >= 3:
                next_row.append("#")
            elif acre == "#" and (lumberyards == 0 or trees == 0):
                next_row.append(".")
            else:
                next_row.append(acre)

        rows.append("".join(next_row))

    return tuple(rows)


def resource_value(grid):
    trees = sum(row.count("|") for row in grid)
    lumberyards = sum(row.count("#") for row in grid)
    return trees * lumberyards


def resource_value_after(part_data, minutes):
    grid = parse_grid(part_data)
    seen = {}
    minute = 0

    while minute < minutes:
        if grid in seen:
            period = minute - seen[grid]
            remaining = minutes - minute
            skip = remaining // period

            if skip:
                minute += skip * period
                continue

        seen[grid] = minute
        grid = step(grid)
        minute += 1

    return resource_value(grid)


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
