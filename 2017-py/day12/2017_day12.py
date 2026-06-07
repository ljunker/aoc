import time

from aocfw import AdventOfCodeClient

YEAR = 2017
DAY = 12


def parse_connections(part_data):
    connections = {}

    for line in part_data.splitlines():
        program, targets = line.split(" <-> ")
        connections[int(program)] = {int(target) for target in targets.split(", ")}

    return connections


def find_group(connections, start):
    group = set()
    queue = [start]

    while queue:
        program = queue.pop()
        if program in group:
            continue

        group.add(program)
        queue.extend(connections[program] - group)

    return group


def part1(part_data):
    connections = parse_connections(part_data)
    return len(find_group(connections, 0))


def part2(part_data):
    connections = parse_connections(part_data)
    remaining = set(connections)
    groups = 0

    while remaining:
        group = find_group(connections, remaining.pop())
        remaining -= group
        groups += 1

    return groups


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
