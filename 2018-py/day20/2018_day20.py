import time
from collections import defaultdict, deque

from aocfw import AdventOfCodeClient

YEAR = 2018
DAY = 20
STEPS = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}


def room_distances(route):
    origin = (0, 0)
    doors = defaultdict(set)
    positions = {origin}
    branches = []

    for token in route.strip()[1:-1]:
        if token == "(":
            branches.append((positions, set()))
        elif token == "|":
            starts, ends = branches[-1]
            ends.update(positions)
            positions = starts
        elif token == ")":
            _, ends = branches.pop()
            ends.update(positions)
            positions = ends
        else:
            dx, dy = STEPS[token]
            destinations = set()
            for x, y in positions:
                destination = (x + dx, y + dy)
                doors[(x, y)].add(destination)
                doors[destination].add((x, y))
                destinations.add(destination)
            positions = destinations

    distances = {origin: 0}
    queue = deque([origin])
    while queue:
        room = queue.popleft()
        for neighbor in doors[room]:
            if neighbor not in distances:
                distances[neighbor] = distances[room] + 1
                queue.append(neighbor)
    return distances


def part1(part_data):
    return max(room_distances(part_data).values())


def part2(part_data):
    return sum(distance >= 1000 for distance in room_distances(part_data).values())


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

