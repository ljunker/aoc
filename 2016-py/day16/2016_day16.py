import time

from aocfw import AdventOfCodeClient

YEAR = 2016
DAY = 16


def dragon_step(data):
    flipped = "".join("1" if bit == "0" else "0" for bit in reversed(data))
    return f"{data}0{flipped}"


def fill_disk(initial_state, disk_size):
    data = initial_state
    while len(data) < disk_size:
        data = dragon_step(data)
    return data[:disk_size]


def checksum(data):
    while len(data) % 2 == 0:
        data = "".join(
            "1" if data[idx] == data[idx + 1] else "0"
            for idx in range(0, len(data), 2)
        )
    return data


def disk_checksum(initial_state, disk_size):
    return checksum(fill_disk(initial_state, disk_size))


def part1(part_data, disk_size=272):
    return disk_checksum(part_data.strip(), disk_size)


def part2(part_data):
    return disk_checksum(part_data.strip(), 35651584)


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
