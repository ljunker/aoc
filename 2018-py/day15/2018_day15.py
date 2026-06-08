import time
from collections import deque
from dataclasses import dataclass

from aocfw import AdventOfCodeClient

YEAR = 2018
DAY = 15

NEIGHBORS = (
    (0, -1),
    (-1, 0),
    (1, 0),
    (0, 1),
)


@dataclass
class Unit:
    kind: str
    x: int
    y: int
    hp: int = 200
    alive: bool = True

    @property
    def position(self):
        return self.x, self.y


def part1(part_data):
    return combat_outcome(part_data)[0]


def part2(part_data):
    attack_power = 4

    while True:
        outcome, elves_died = combat_outcome(part_data, elf_attack=attack_power)
        if not elves_died:
            return outcome

        attack_power += 1


def reading_order(position):
    x, y = position
    return y, x


def adjacent(position):
    x, y = position
    return [
        (x + dx, y + dy)
        for dx, dy in NEIGHBORS
    ]


def parse_map(part_data):
    walls = set()
    units = []

    for y, line in enumerate(part_data.strip("\n").splitlines()):
        for x, char in enumerate(line):
            if char == "#":
                walls.add((x, y))
            elif char in "EG":
                units.append(Unit(char, x, y))

    return walls, units


def open_square(position, walls, occupied):
    return position not in walls and position not in occupied


def alive_units(units):
    return [
        unit
        for unit in units
        if unit.alive
    ]


def occupied_positions(units, ignore=None):
    return {
        unit.position
        for unit in alive_units(units)
        if unit is not ignore
    }


def bfs_distances(start, walls, occupied):
    distances = {start: 0}
    queue = deque([start])

    while queue:
        position = queue.popleft()

        for neighbor in adjacent(position):
            if neighbor in distances or not open_square(neighbor, walls, occupied):
                continue

            distances[neighbor] = distances[position] + 1
            queue.append(neighbor)

    return distances


def choose_move(unit, units, walls):
    enemies = [
        other
        for other in alive_units(units)
        if other.kind != unit.kind
    ]
    occupied = occupied_positions(units, ignore=unit)
    target_squares = {
        position
        for enemy in enemies
        for position in adjacent(enemy.position)
        if open_square(position, walls, occupied)
    }

    distances = bfs_distances(unit.position, walls, occupied)
    reachable_targets = [
        target
        for target in target_squares
        if target in distances
    ]

    if not reachable_targets:
        return None

    target = min(
        reachable_targets,
        key=lambda position: (distances[position], reading_order(position)),
    )
    target_distances = bfs_distances(target, walls, occupied)
    steps = [
        step
        for step in adjacent(unit.position)
        if step in target_distances and open_square(step, walls, occupied)
    ]

    if not steps:
        return None

    return min(
        steps,
        key=lambda position: (target_distances[position], reading_order(position)),
    )


def adjacent_enemies(unit, units):
    positions = set(adjacent(unit.position))
    return [
        other
        for other in alive_units(units)
        if other.kind != unit.kind and other.position in positions
    ]


def attack(unit, units, elf_attack):
    enemies = adjacent_enemies(unit, units)
    if not enemies:
        return False

    target = min(
        enemies,
        key=lambda enemy: (enemy.hp, reading_order(enemy.position)),
    )
    damage = elf_attack if unit.kind == "E" else 3
    target.hp -= damage

    if target.hp > 0:
        return False

    target.alive = False
    return target.kind == "E"


def take_turn(unit, units, walls, elf_attack):
    if not adjacent_enemies(unit, units):
        step = choose_move(unit, units, walls)
        if step is not None:
            unit.x, unit.y = step

    return attack(unit, units, elf_attack)


def combat_outcome(part_data, elf_attack=3):
    walls, units = parse_map(part_data)
    rounds = 0
    elves_died = False

    while True:
        units.sort(key=lambda unit: reading_order(unit.position))

        for unit in units:
            if not unit.alive:
                continue

            if not any(other.alive and other.kind != unit.kind for other in units):
                hp_left = sum(other.hp for other in alive_units(units))
                return rounds * hp_left, elves_died

            elves_died = take_turn(unit, units, walls, elf_attack) or elves_died

        rounds += 1


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
