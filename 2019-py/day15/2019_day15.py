import time
from collections import deque

from aocfw import AdventOfCodeClient
from IntComputer.computer import IntComputer

YEAR = 2019
DAY = 15

ORIGIN = 0j
DIRECTIONS = {1: -1j, 2: 1j, 3: -1, 4: 1}
REVERSE = {1: 2, 2: 1, 3: 4, 4: 3}


def explore(move):
    tiles = {ORIGIN: 1}
    oxygen = None
    path = [(ORIGIN, None, iter(DIRECTIONS))]

    while path:
        position, return_command, commands = path[-1]
        command = next(commands, None)
        if command is None:
            path.pop()
            if return_command is not None:
                move(return_command)
            continue

        neighbor = position + DIRECTIONS[command]
        if neighbor in tiles:
            continue

        status = move(command)
        tiles[neighbor] = status
        if status == 0:
            continue
        if status == 2:
            oxygen = neighbor
        path.append((neighbor, REVERSE[command], iter(DIRECTIONS)))

    if oxygen is None:
        raise ValueError("Oxygen system not found")
    return tiles, oxygen


def oxygen_distances(tiles, oxygen):
    distances = {oxygen: 0}
    queue = deque([oxygen])
    while queue:
        position = queue.popleft()
        for direction in DIRECTIONS.values():
            neighbor = position + direction
            if tiles.get(neighbor) and neighbor not in distances:
                distances[neighbor] = distances[position] + 1
                queue.append(neighbor)
    return distances


def solve(data):
    computer = IntComputer(
        map(int, data.strip().split(",")),
        input_piped_mode=True,
        output_piped_mode=True,
    )

    def move(command):
        computer.piped_input.append(command)
        computer.run_program()
        return computer.piped_output.pop()

    tiles, oxygen = explore(move)
    distances = oxygen_distances(tiles, oxygen)
    return distances[ORIGIN], max(distances.values())


if __name__ == "__main__":
    client = AdventOfCodeClient()
    first, second = solve(client.get_input(YEAR, DAY))

    print("Part 1:", first)
    res = client.submit_answer(YEAR, DAY, 1, first)
    print(res.message)

    time.sleep(10)

    print("Part 2:", second)
    res = client.submit_answer(YEAR, DAY, 2, second)
    print(res.message)
