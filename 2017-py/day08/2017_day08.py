import time
from collections import defaultdict
from operator import eq, ge, gt, le, lt, ne

from aocfw import AdventOfCodeClient

YEAR = 2017
DAY = 8

CONDITIONS = {
    ">": gt,
    "<": lt,
    ">=": ge,
    "<=": le,
    "==": eq,
    "!=": ne,
}


def run(part_data):
    registers = defaultdict(int)
    highest_seen = 0

    for line in part_data.splitlines():
        register, operation, value, _, condition_register, condition, condition_value = line.split()

        if CONDITIONS[condition](registers[condition_register], int(condition_value)):
            if operation == "dec":
                value = -int(value)
            else:
                value = int(value)

            registers[register] += value
            highest_seen = max(highest_seen, registers[register])

    return max(registers.values()), highest_seen


def part1(part_data):
    return run(part_data)[0]


def part2(part_data):
    return run(part_data)[1]


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
