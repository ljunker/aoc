import time

from aocfw import AdventOfCodeClient

YEAR = 2017
DAY = 22

DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def parse_grid(part_data):
    lines = part_data.splitlines()
    offset = len(lines) // 2
    infected = set()

    for y, line in enumerate(lines):
        for x, value in enumerate(line):
            if value == "#":
                infected.add((x - offset, y - offset))

    return infected


def infections_after_bursts(part_data, bursts):
    infected = parse_grid(part_data)
    x = 0
    y = 0
    direction = 0
    infections = 0

    for _ in range(bursts):
        position = (x, y)

        if position in infected:
            direction = (direction + 1) % 4
            infected.remove(position)
        else:
            direction = (direction - 1) % 4
            infected.add(position)
            infections += 1

        dx, dy = DIRECTIONS[direction]
        x += dx
        y += dy

    return infections


def evolved_infections_after_bursts(part_data, bursts):
    states = {position: "#" for position in parse_grid(part_data)}
    x = 0
    y = 0
    direction = 0
    infections = 0

    for _ in range(bursts):
        position = (x, y)
        state = states.get(position, ".")

        if state == ".":
            direction = (direction - 1) % 4
            states[position] = "W"
        elif state == "W":
            states[position] = "#"
            infections += 1
        elif state == "#":
            direction = (direction + 1) % 4
            states[position] = "F"
        else:
            direction = (direction + 2) % 4
            states.pop(position)

        dx, dy = DIRECTIONS[direction]
        x += dx
        y += dy

    return infections


def part1(part_data):
    return infections_after_bursts(part_data, 10_000)


def part2(part_data):
    return evolved_infections_after_bursts(part_data, 10_000_000)


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
