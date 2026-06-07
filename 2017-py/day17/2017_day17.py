import time

from aocfw import AdventOfCodeClient

YEAR = 2017
DAY = 17


def spinlock_value_after_last(step_size, insertions=2017):
    buffer = [0]
    position = 0

    for value in range(1, insertions + 1):
        position = (position + step_size) % len(buffer) + 1
        buffer.insert(position, value)

    return buffer[(position + 1) % len(buffer)]


def spinlock_value_after_zero(step_size, insertions=50_000_000):
    position = 0
    value_after_zero = None

    for value in range(1, insertions + 1):
        position = (position + step_size) % value + 1
        if position == 1:
            value_after_zero = value

    return value_after_zero


def part1(part_data):
    return spinlock_value_after_last(int(part_data.strip()))


def part2(part_data):
    return spinlock_value_after_zero(int(part_data.strip()))


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
