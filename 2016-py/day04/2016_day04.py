import string

from aocfw import AdventOfCodeClient, SubmissionStatus
from collections import Counter

YEAR = 2016
DAY = 4


def part1(part_data):
    total = 0
    lines = part_data.split("\n")
    for line in lines:
        room, checksum = line.split("[")
        checksum = checksum.strip("]")
        room = room.split("-")
        room, sector = ''.join(room[:-1]), int(room[-1])
        counts = Counter(room).most_common()
        counts = sorted(counts, key=lambda x: (-x[1], x[0]))
        if checksum == ''.join([c[0] for c in counts[:5]]):
            total += sector
    return total


def decrypt(room, sector):
    sector = sector % 26
    alphabet = string.ascii_lowercase
    shifted_alphabet = alphabet[sector:] + alphabet[:sector]
    table = str.maketrans(alphabet, shifted_alphabet)
    return room.translate(table)

def part2(part_data):
    lines = part_data.split("\n")
    for line in lines:
        room, checksum = line.split("[")
        checksum = checksum.strip("]")
        room = room.split("-")
        room, sector = ''.join(room[:-1]), int(room[-1])
        counts = Counter(room).most_common()
        counts = sorted(counts, key=lambda x: (-x[1], x[0]))
        if checksum == ''.join([c[0] for c in counts[:5]]):
            if decrypt(room, sector) == 'northpoleobjectstorage':
                return sector


if __name__ == "__main__":
    client = AdventOfCodeClient()

    data = client.get_input(YEAR, DAY)
    answer = part1(data)
    print("Part 1:", answer)
    # res = client.submit_answer(YEAR, DAY, 1, answer)
    # print(res.message)

    answer = part2(data)
    print("Part 2:", answer)
    res = client.submit_answer(YEAR, DAY, 2, answer)
    print(res.message)
