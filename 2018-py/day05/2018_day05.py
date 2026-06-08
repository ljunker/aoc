import time

from aocfw import AdventOfCodeClient

YEAR = 2018
DAY = 5


def reacts(left, right):
    return left != right and left.lower() == right.lower()


def reacted_length(polymer):
    stack = []

    for unit in polymer:
        if stack and reacts(stack[-1], unit):
            stack.pop()
        else:
            stack.append(unit)

    return len(stack)


def part1(part_data):
    return reacted_length(part_data.strip())


def part2(part_data):
    polymer = part_data.strip()
    return min(
        reacted_length(unit for unit in polymer if unit.lower() != unit_type)
        for unit_type in "abcdefghijklmnopqrstuvwxyz"
    )


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
