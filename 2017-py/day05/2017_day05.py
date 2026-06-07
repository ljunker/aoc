import time

from aocfw import AdventOfCodeClient

YEAR = 2017
DAY = 5


def parse_offsets(part_data):
    return [int(line) for line in part_data.splitlines() if line.strip()]


def steps_to_exit(part_data, strange=False):
    offsets = parse_offsets(part_data)
    pointer = 0
    steps = 0

    while 0 <= pointer < len(offsets):
        jump = offsets[pointer]
        offsets[pointer] += -1 if strange and jump >= 3 else 1
        pointer += jump
        steps += 1

    return steps


def part1(part_data):
    return steps_to_exit(part_data)


def part2(part_data):
    return steps_to_exit(part_data, strange=True)


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
