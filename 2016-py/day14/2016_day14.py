import time
import hashlib
from functools import cache

from aocfw import AdventOfCodeClient

YEAR = 2016
DAY = 14


def md5_hex(data):
    return hashlib.md5(data.encode()).hexdigest()


def first_triple(hash_value):
    for idx in range(len(hash_value) - 2):
        if hash_value[idx] == hash_value[idx + 1] == hash_value[idx + 2]:
            return hash_value[idx]
    return None


def key_index(salt, stretch_rounds=0, target_keys=64):
    @cache
    def hash_for(idx):
        hash_value = md5_hex(f"{salt}{idx}")
        for _ in range(stretch_rounds):
            hash_value = md5_hex(hash_value)
        return hash_value

    keys = []
    idx = 0
    while len(keys) < target_keys:
        hash_value = hash_for(idx)
        triple = first_triple(hash_value)
        if triple is not None:
            quintuple = triple * 5
            if any(
                quintuple in hash_for(candidate)
                for candidate in range(idx + 1, idx + 1001)
            ):
                keys.append(idx)
        idx += 1

    return keys[-1]


def part1(part_data):
    return key_index(part_data.strip())


def part2(part_data):
    return key_index(part_data.strip(), 2016)


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
