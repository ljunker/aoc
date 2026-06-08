import time

from aocfw import AdventOfCodeClient

YEAR = 2018
DAY = 11


def part1(part_data):
    serial = int(part_data)
    grid = build_summed_grid(serial)
    x, y, _ = best_square(grid, 3)
    return f"{x},{y}"


def part2(part_data):
    serial = int(part_data)
    grid = build_summed_grid(serial)
    best = None

    for size in range(1, 301):
        current = best_square(grid, size)
        if best is None or current[2] > best[3]:
            best = current[0], current[1], size, current[2]

    return f"{best[0]},{best[1]},{best[2]}"


def power_level(x, y, serial):
    rack_id = x + 10
    power = (rack_id * y + serial) * rack_id
    return power // 100 % 10 - 5


def build_summed_grid(serial):
    grid = [[0] * 301 for _ in range(301)]

    for y in range(1, 301):
        row_sum = 0
        for x in range(1, 301):
            row_sum += power_level(x, y, serial)
            grid[y][x] = grid[y - 1][x] + row_sum

    return grid


def square_power(grid, x, y, size):
    max_x = x + size - 1
    max_y = y + size - 1
    return (
        grid[max_y][max_x]
        - grid[y - 1][max_x]
        - grid[max_y][x - 1]
        + grid[y - 1][x - 1]
    )


def best_square(grid, size):
    best = None

    for y in range(1, 302 - size):
        for x in range(1, 302 - size):
            total = square_power(grid, x, y, size)
            if best is None or total > best[2]:
                best = x, y, total

    return best


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
