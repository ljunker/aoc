import hashlib
from collections import Counter

from aocfw import AdventOfCodeClient

YEAR = 2016
DAY = 6



def part1(part_data):
    lines = part_data.split('\n')
    codewords = []
    for i in range(len(lines[0])):
        codewords.append([line[i] for _, line in enumerate(lines)])
    for codeword in codewords:
        print(Counter(codeword).most_common(1))
    answer = ''.join([Counter(codeword).most_common(1)[0][0] for codeword in codewords])
    return answer

def part2(part_data):
    lines = part_data.split('\n')
    codewords = []
    for i in range(len(lines[0])):
        codewords.append([line[i] for _, line in enumerate(lines)])
    for codeword in codewords:
        print(Counter(codeword).most_common())
    answer = ''.join([Counter(codeword).most_common()[-1][0] for codeword in codewords])
    return answer


if __name__ == "__main__":
    client = AdventOfCodeClient()

    data = client.get_input(YEAR, DAY)
    # answer = part1(data)
    # print("Part 1:", answer)
    # res = client.submit_answer(YEAR, DAY, 1, answer)
    # print(res.message)

    answer = part2(data)
    print("Part 2:", answer)
    # res = client.submit_answer(YEAR, DAY, 2, answer)
    # print(res.message)
