import time
from collections import Counter

from aocfw import AdventOfCodeClient

YEAR = 2017
DAY = 7


def parse_programs(part_data):
    weights = {}
    children = {}

    for line in part_data.splitlines():
        if not line.strip():
            continue

        left, _, right = line.partition(" -> ")
        name, weight = left.split()
        weights[name] = int(weight.strip("()"))
        children[name] = right.split(", ") if right else []

    return weights, children


def root_program(weights, children):
    all_children = {
        child
        for child_names in children.values()
        for child in child_names
    }
    return (set(weights) - all_children).pop()


def find_correct_weight(weights, children, name):
    for child in children[name]:
        correction = find_correct_weight(weights, children, child)
        if correction is not None:
            return correction

    totals = {
        child: total_weight(weights, children, child)
        for child in children[name]
    }
    counts = Counter(totals.values())
    if len(counts) <= 1:
        return None

    correct_total = counts.most_common(1)[0][0]
    wrong_total = next(total for total, count in counts.items() if count == 1)
    wrong_child = next(child for child, total in totals.items() if total == wrong_total)
    return weights[wrong_child] + correct_total - wrong_total


def total_weight(weights, children, name):
    return weights[name] + sum(
        total_weight(weights, children, child)
        for child in children[name]
    )


def part1(part_data):
    weights, children = parse_programs(part_data)
    return root_program(weights, children)


def part2(part_data):
    weights, children = parse_programs(part_data)
    return find_correct_weight(weights, children, root_program(weights, children))


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
