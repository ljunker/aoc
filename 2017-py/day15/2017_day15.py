import time

from aocfw import AdventOfCodeClient

YEAR = 2017
DAY = 15

FACTOR_A = 16807
FACTOR_B = 48271
DIVISOR = 2147483647
LOWER_16_BITS = 0xFFFF


def parse_starts(part_data):
    return [int(line.split()[-1]) for line in part_data.splitlines()]


def judge_count(starts, pairs, multiple_a=1, multiple_b=1):
    a, b = starts
    matches = 0

    if multiple_a == 1 and multiple_b == 1:
        for _ in range(pairs):
            a = (a * FACTOR_A) % DIVISOR
            b = (b * FACTOR_B) % DIVISOR

            if a & LOWER_16_BITS == b & LOWER_16_BITS:
                matches += 1

        return matches

    for _ in range(pairs):
        a = (a * FACTOR_A) % DIVISOR
        while a % multiple_a:
            a = (a * FACTOR_A) % DIVISOR

        b = (b * FACTOR_B) % DIVISOR
        while b % multiple_b:
            b = (b * FACTOR_B) % DIVISOR

        if a & LOWER_16_BITS == b & LOWER_16_BITS:
            matches += 1

    return matches


def part1(part_data):
    return judge_count(parse_starts(part_data), 40_000_000)


def part2(part_data):
    return judge_count(parse_starts(part_data), 5_000_000, 4, 8)


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
