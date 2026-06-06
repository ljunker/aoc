import time

from aocfw import AdventOfCodeClient

YEAR = 2016
DAY = 20
MAX_IP = 4294967295


def parse_ranges(part_data):
    ranges = []
    for line in part_data.splitlines():
        if not line.strip():
            continue

        start, end = line.split("-")
        ranges.append((int(start), int(end)))

    return sorted(ranges)


def first_allowed_ip(part_data):
    candidate = 0

    for start, end in parse_ranges(part_data):
        if candidate < start:
            return candidate
        if candidate <= end:
            candidate = end + 1

    return candidate


def count_allowed_ips(part_data, max_ip=MAX_IP):
    allowed = 0
    candidate = 0

    for start, end in parse_ranges(part_data):
        if start > max_ip:
            break
        if candidate < start:
            allowed += start - candidate
        if candidate <= end:
            candidate = min(end, max_ip) + 1

    if candidate <= max_ip:
        allowed += max_ip - candidate + 1

    return allowed


def part1(part_data):
    return first_allowed_ip(part_data)


def part2(part_data, max_ip=MAX_IP):
    return count_allowed_ips(part_data, max_ip)


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
