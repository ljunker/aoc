import time

from aocfw import AdventOfCodeClient

YEAR = 2016
DAY = 19


def winning_elf_left(count):
    highest_power = 1 << (count.bit_length() - 1)
    return 2 * (count - highest_power) + 1


def winning_elf_across(count):
    highest_power = 1
    while highest_power * 3 <= count:
        highest_power *= 3

    if count == highest_power:
        return count
    if count <= 2 * highest_power:
        return count - highest_power
    return 2 * count - 3 * highest_power


def part1(part_data):
    return winning_elf_left(int(part_data))


def part2(part_data):
    return winning_elf_across(int(part_data))


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
