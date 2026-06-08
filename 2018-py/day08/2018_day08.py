import time

from aocfw import AdventOfCodeClient

YEAR = 2018
DAY = 8


def parse_numbers(part_data):
    return list(map(int, part_data.split()))


def read_node(numbers, index=0):
    child_count = numbers[index]
    metadata_count = numbers[index + 1]
    index += 2
    metadata_sum = 0
    child_values = []

    for _ in range(child_count):
        index, child_metadata_sum, child_value = read_node(numbers, index)
        metadata_sum += child_metadata_sum
        child_values.append(child_value)

    metadata = numbers[index : index + metadata_count]
    index += metadata_count
    metadata_sum += sum(metadata)

    if child_count == 0:
        value = sum(metadata)
    else:
        value = sum(
            child_values[entry - 1]
            for entry in metadata
            if 1 <= entry <= len(child_values)
        )

    return index, metadata_sum, value


def part1(part_data):
    return read_node(parse_numbers(part_data))[1]


def part2(part_data):
    return read_node(parse_numbers(part_data))[2]


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
