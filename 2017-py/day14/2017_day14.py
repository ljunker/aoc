import time

from aocfw import AdventOfCodeClient

YEAR = 2017
DAY = 14


def run_round(numbers, lengths, position=0, skip_size=0):
    size = len(numbers)

    for length in lengths:
        for offset in range(length // 2):
            left = (position + offset) % size
            right = (position + length - 1 - offset) % size
            numbers[left], numbers[right] = numbers[right], numbers[left]

        position = (position + length + skip_size) % size
        skip_size += 1

    return position, skip_size


def knot_hash(part_data):
    numbers = list(range(256))
    lengths = [ord(char) for char in part_data.strip()] + [17, 31, 73, 47, 23]
    position = 0
    skip_size = 0

    for _ in range(64):
        position, skip_size = run_round(numbers, lengths, position, skip_size)

    dense_hash = []
    for block_start in range(0, len(numbers), 16):
        block = numbers[block_start : block_start + 16]
        value = 0
        for number in block:
            value ^= number
        dense_hash.append(value)

    return "".join(f"{value:02x}" for value in dense_hash)


def disk_rows(key):
    rows = []

    for row in range(128):
        hash_value = knot_hash(f"{key}-{row}")
        rows.append("".join(f"{int(digit, 16):04b}" for digit in hash_value))

    return rows


def part1(part_data):
    return sum(row.count("1") for row in disk_rows(part_data.strip()))


def part2(part_data):
    rows = disk_rows(part_data.strip())
    used = {
        (x, y)
        for y, row in enumerate(rows)
        for x, value in enumerate(row)
        if value == "1"
    }
    regions = 0

    while used:
        regions += 1
        queue = [used.pop()]

        while queue:
            x, y = queue.pop()
            for neighbor in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if neighbor in used:
                    used.remove(neighbor)
                    queue.append(neighbor)

    return regions


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
