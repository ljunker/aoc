import time

from aocfw import AdventOfCodeClient

YEAR = 2017
DAY = 21

START = (".#.", "..#", "###")


def rotate(pattern):
    size = len(pattern)
    return tuple(
        "".join(pattern[size - 1 - y][x] for y in range(size))
        for x in range(size)
    )


def flip(pattern):
    return tuple(row[::-1] for row in pattern)


def variants(pattern):
    current = pattern
    result = set()

    for _ in range(4):
        result.add(current)
        result.add(flip(current))
        current = rotate(current)

    return result


def parse_rules(part_data):
    rules = {}

    for line in part_data.splitlines():
        source, target = line.split(" => ")
        source_pattern = tuple(source.split("/"))
        target_pattern = tuple(target.split("/"))

        for variant in variants(source_pattern):
            rules[variant] = target_pattern

    return rules


def enhance(pattern, rules):
    size = len(pattern)
    block_size = 2 if size % 2 == 0 else 3
    output_block_size = block_size + 1
    blocks_per_side = size // block_size
    output = []

    for block_y in range(blocks_per_side):
        rows = [""] * output_block_size

        for block_x in range(blocks_per_side):
            block = tuple(
                pattern[block_y * block_size + y][
                    block_x * block_size : (block_x + 1) * block_size
                ]
                for y in range(block_size)
            )
            replacement = rules[block]

            for y, row in enumerate(replacement):
                rows[y] += row

        output.extend(rows)

    return tuple(output)


def count_pixels(part_data, iterations):
    rules = parse_rules(part_data)
    pattern = START

    for _ in range(iterations):
        pattern = enhance(pattern, rules)

    return sum(row.count("#") for row in pattern)


def part1(part_data):
    return count_pixels(part_data, 5)


def part2(part_data):
    return count_pixels(part_data, 18)


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
