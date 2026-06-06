import time

from aocfw import AdventOfCodeClient

YEAR = 2017
DAY = 1


def captcha_sum(part_data, step):
    digits = part_data.strip()
    return sum(
        int(digit)
        for index, digit in enumerate(digits)
        if digit == digits[(index + step) % len(digits)]
    )


def part1(part_data):
    return captcha_sum(part_data, 1)


def part2(part_data):
    return captcha_sum(part_data, len(part_data.strip()) // 2)


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
