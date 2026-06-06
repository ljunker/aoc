import time

from aocfw import AdventOfCodeClient

YEAR = 2016
DAY = 9


def compressed_data(part_data):
    return "".join(part_data.split())


def decompressed_length(data, recursive=False):
    total = 0
    idx = 0

    while idx < len(data):
        if data[idx] != "(":
            total += 1
            idx += 1
            continue

        marker_end = data.index(")", idx)
        size, repeats = [
            int(num)
            for num in data[idx + 1:marker_end].split("x")
        ]
        segment_start = marker_end + 1
        segment_end = segment_start + size
        segment = data[segment_start:segment_end]

        if recursive:
            total += repeats * decompressed_length(segment, True)
        else:
            total += repeats * size
        idx = segment_end

    return total


def part1(part_data):
    return decompressed_length(compressed_data(part_data))


def part2(part_data):
    return decompressed_length(compressed_data(part_data), True)


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
