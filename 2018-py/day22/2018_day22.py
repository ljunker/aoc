import time
from heapq import heappop, heappush

from aocfw import AdventOfCodeClient

YEAR = 2018
DAY = 22

NEITHER, TORCH, CLIMBING_GEAR = range(3)
ALLOWED = (
    {TORCH, CLIMBING_GEAR},
    {NEITHER, CLIMBING_GEAR},
    {NEITHER, TORCH},
)


def parse_input(part_data):
    depth, target = part_data.strip().splitlines()
    x, y = map(int, target.split()[1].split(","))
    return int(depth.split()[1]), (x, y)


class Cave:
    def __init__(self, depth, target):
        self.depth = depth
        self.target = target
        self.rows = []
        self.width = 0

    def region(self, x, y):
        if y >= len(self.rows) or x >= self.width:
            width = max(self.width, x + 1)
            height = max(len(self.rows), y + 1)
            self.rows.extend([] for _ in range(height - len(self.rows)))
            for row_y, row in enumerate(self.rows):
                for column in range(len(row), width):
                    if (column, row_y) in ((0, 0), self.target):
                        index = 0
                    elif row_y == 0:
                        index = column * 16807
                    elif column == 0:
                        index = row_y * 48271
                    else:
                        index = row[-1] * self.rows[row_y - 1][column]
                    row.append((index + self.depth) % 20183)
            self.width = width
        return self.rows[y][x] % 3


def part1(part_data):
    cave = Cave(*parse_input(part_data))
    target_x, target_y = cave.target
    cave.region(target_x, target_y)
    return sum(
        cave.region(x, y)
        for y in range(target_y + 1)
        for x in range(target_x + 1)
    )


def part2(part_data):
    cave = Cave(*parse_input(part_data))
    target_x, target_y = cave.target
    goal = (target_x, target_y, TORCH)
    start = (0, 0, TORCH)
    distances = {start: 0}
    queue = [(target_x + target_y, 0, start)]

    while queue:
        _, minutes, state = heappop(queue)
        if minutes != distances[state]:
            continue
        if state == goal:
            return minutes

        x, y, tool = state
        allowed = ALLOWED[cave.region(x, y)]
        moves = [((x, y, replacement), 7) for replacement in allowed if replacement != tool]
        for next_x, next_y in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if next_x >= 0 and next_y >= 0 and tool in ALLOWED[cave.region(next_x, next_y)]:
                moves.append(((next_x, next_y, tool), 1))

        for destination, cost in moves:
            arrival = minutes + cost
            if arrival < distances.get(destination, float("inf")):
                distances[destination] = arrival
                next_x, next_y, next_tool = destination
                estimate = abs(target_x - next_x) + abs(target_y - next_y)
                if next_tool != TORCH:
                    estimate += 7
                heappush(queue, (arrival + estimate, arrival, destination))


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

