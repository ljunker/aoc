import time

from aocfw import AdventOfCodeClient

YEAR = 2016
DAY = 18

TRAP_PATTERNS = {"^^.", ".^^", "^..", "..^"}


def next_row(row):
    padded = f".{row}."
    return "".join(
        "^" if padded[idx:idx + 3] in TRAP_PATTERNS else "."
        for idx in range(len(row))
    )


def count_safe_tiles(first_row, rows):
    row = first_row.strip()
    safe_tiles = row.count(".")

    for _ in range(rows - 1):
        row = next_row(row)
        safe_tiles += row.count(".")

    return safe_tiles


def part1(part_data, rows=40):
    return count_safe_tiles(part_data, rows)


def part2(part_data):
    return count_safe_tiles(part_data, 400000)


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
