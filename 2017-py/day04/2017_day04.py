import time

from aocfw import AdventOfCodeClient

YEAR = 2017
DAY = 4


def passphrases(part_data):
    return [
        line.split()
        for line in part_data.splitlines()
        if line.strip()
    ]


def has_no_duplicates(words):
    return len(words) == len(set(words))


def has_no_anagrams(words):
    signatures = ["".join(sorted(word)) for word in words]
    return len(signatures) == len(set(signatures))


def part1(part_data):
    return sum(has_no_duplicates(words) for words in passphrases(part_data))


def part2(part_data):
    return sum(has_no_anagrams(words) for words in passphrases(part_data))


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
