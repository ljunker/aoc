import hashlib
import re
from collections import Counter

from sympy import andre

from aocfw import AdventOfCodeClient

YEAR = 2016
DAY = 7

pattern = re.compile(r'(.)(?!\1)(.)\2\1')


def has_abba(part):
    return pattern.search(part)


def has_tls(line):
    parts = re.split(r'[\[\]]', line)
    outside_parts_with_abba = [part for i, part in enumerate(parts) if i % 2 == 0 and has_abba(part)]
    inside_parts_with_abba = [part for i, part in enumerate(parts) if i % 2 == 1 and has_abba(part)]
    return len(outside_parts_with_abba) > 0 and len(inside_parts_with_abba) == 0


def part1(part_data):
    return len([line for line in part_data.split('\n') if has_tls(line)])


aba_re = re.compile(r'(?=((.)(?!\2)(.)\2))')


def find_abas(s):
    return [m.group(1) for m in aba_re.finditer(s)]


def aba_to_bab(aba: str) -> str:
    return aba[1] + aba[0] + aba[1]


def has_ssl(line):
    parts = re.split(r'[\[\]]', line)
    outside_parts = [part for i, part in enumerate(parts) if i % 2 == 0]
    inside_parts = [part for i, part in enumerate(parts) if i % 2 == 1]
    candidates = [
        aba_to_bab(cand)
        for part in outside_parts
        for cand in find_abas(part)
    ]
    return any(
        bab in part
        for part in inside_parts
        for bab in candidates
    )


def part2(part_data):
    return len([line for line in part_data.split('\n') if has_ssl(line)])


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
