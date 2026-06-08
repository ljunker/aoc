import time
import re
from collections import Counter
from dataclasses import dataclass

from aocfw import AdventOfCodeClient

YEAR = 2018
DAY = 3


@dataclass(frozen=True)
class Claim:
    claim_id: int
    left: int
    top: int
    width: int
    height: int

    def coordinates(self):
        for x in range(self.left, self.left + self.width):
            for y in range(self.top, self.top + self.height):
                yield x, y


def parse_claims(part_data):
    claims = []

    for line in part_data.splitlines():
        claim_id, left, top, width, height = map(int, re.findall(r"\d+", line))
        claims.append(Claim(claim_id, left, top, width, height))

    return claims


def fabric_counts(claims):
    counts = Counter()

    for claim in claims:
        counts.update(claim.coordinates())

    return counts


def part1(part_data):
    return sum(count > 1 for count in fabric_counts(parse_claims(part_data)).values())


def part2(part_data):
    claims = parse_claims(part_data)
    counts = fabric_counts(claims)

    for claim in claims:
        if all(counts[coordinate] == 1 for coordinate in claim.coordinates()):
            return claim.claim_id


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
