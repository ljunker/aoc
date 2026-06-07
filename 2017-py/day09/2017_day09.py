import time

from aocfw import AdventOfCodeClient

YEAR = 2017
DAY = 9


def scan_stream(part_data):
    score = 0
    depth = 0
    garbage_chars = 0
    in_garbage = False
    canceled = False

    for char in part_data.strip():
        if canceled:
            canceled = False
            continue

        if in_garbage:
            if char == "!":
                canceled = True
            elif char == ">":
                in_garbage = False
            else:
                garbage_chars += 1
            continue

        if char == "<":
            in_garbage = True
        elif char == "{":
            depth += 1
            score += depth
        elif char == "}":
            depth -= 1

    return score, garbage_chars


def part1(part_data):
    return scan_stream(part_data)[0]


def part2(part_data):
    return scan_stream(part_data)[1]


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
