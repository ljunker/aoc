import time
from collections import deque
from itertools import permutations

from aocfw import AdventOfCodeClient

YEAR = 2016
DAY = 24


def parse_grid(part_data):
    grid = [line for line in part_data.splitlines() if line]
    locations = {}

    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            if tile.isdigit():
                locations[tile] = (x, y)

    return grid, locations


def neighbors(position):
    x, y = position
    yield x - 1, y
    yield x + 1, y
    yield x, y - 1
    yield x, y + 1


def distances_from(grid, start):
    queue = deque([(start, 0)])
    seen = {start}
    distances = {}

    while queue:
        position, steps = queue.popleft()
        distances[position] = steps

        for next_position in neighbors(position):
            x, y = next_position
            if (
                next_position not in seen
                and 0 <= y < len(grid)
                and 0 <= x < len(grid[y])
                and grid[y][x] != "#"
            ):
                seen.add(next_position)
                queue.append((next_position, steps + 1))

    return distances


def pair_distances(grid, locations):
    distances = {}
    for source, position in locations.items():
        all_distances = distances_from(grid, position)
        for target, target_position in locations.items():
            if source != target:
                distances[source, target] = all_distances[target_position]

    return distances


def shortest_route(part_data, return_home=False):
    grid, locations = parse_grid(part_data)
    distances = pair_distances(grid, locations)
    targets = sorted(location for location in locations if location != "0")
    best = None

    for order in permutations(targets):
        route = ("0",) + order
        steps = sum(
            distances[source, target]
            for source, target in zip(route, route[1:])
        )
        if return_home:
            steps += distances[route[-1], "0"]

        if best is None or steps < best:
            best = steps

    return best


def part1(part_data):
    return shortest_route(part_data)


def part2(part_data):
    return shortest_route(part_data, return_home=True)


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
