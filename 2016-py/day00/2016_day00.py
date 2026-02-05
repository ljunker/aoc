from aocfw import AdventOfCodeClient

YEAR = 2016
DAY = 7


def part1(part_data):
    return 0


def part2(part_data):
    return 0


if __name__ == "__main__":
    client = AdventOfCodeClient()

    data = client.get_input(YEAR, DAY)
    answer = part1(data)
    print("Part 1:", answer)
    # res = client.submit_answer(YEAR, DAY, 1, answer)
    # print(res.message)

    answer = part2(data)
    print("Part 2:", answer)
    # res = client.submit_answer(YEAR, DAY, 2, answer)
    # print(res.message)
