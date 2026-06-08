import time

from aocfw import AdventOfCodeClient

YEAR = 2018
DAY = 12


def part1(part_data):
    return plant_score(part_data, 20)


def part2(part_data):
    return plant_score(part_data, 50_000_000_000)


def parse_input(part_data):
    lines = part_data.strip().splitlines()
    plants = {
        index
        for index, state in enumerate(lines[0].removeprefix("initial state: "))
        if state == "#"
    }
    rules = {
        pattern
        for line in lines[2:]
        for pattern, result in [line.split(" => ")]
        if result == "#"
    }
    return plants, rules


def next_generation(plants, rules):
    return {
        index
        for index in range(min(plants) - 2, max(plants) + 3)
        if "".join(
            "#" if pot in plants else "."
            for pot in range(index - 2, index + 3)
        ) in rules
    }


def normalized(plants):
    first = min(plants)
    return tuple(sorted(pot - first for pot in plants)), first


def plant_score(part_data, generations):
    plants, rules = parse_input(part_data)
    seen = {}
    generation = 0

    while generation < generations:
        shape, first = normalized(plants)

        if shape in seen:
            previous_generation, previous_first = seen[shape]
            period = generation - previous_generation
            shift = first - previous_first
            cycles = (generations - generation) // period

            if cycles:
                plants = {
                    pot + shift * cycles
                    for pot in plants
                }
                generation += period * cycles
                continue

        seen[shape] = generation, first
        plants = next_generation(plants, rules)
        generation += 1

    return sum(plants)


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
