import time

from aocfw import AdventOfCodeClient

YEAR = 2017
DAY = 13


def parse_firewall(part_data):
    firewall = []

    for line in part_data.splitlines():
        depth, scanner_range = line.split(": ")
        firewall.append((int(depth), int(scanner_range)))

    return firewall


def caught(depth, scanner_range, delay=0):
    cycle = 2 * (scanner_range - 1)
    return cycle == 0 or (depth + delay) % cycle == 0


def part1(part_data):
    return sum(depth * scanner_range for depth, scanner_range in parse_firewall(part_data) if caught(depth, scanner_range))


def part2(part_data):
    firewall = parse_firewall(part_data)
    delay = 0

    while any(caught(depth, scanner_range, delay) for depth, scanner_range in firewall):
        delay += 1

    return delay


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
