import time
from collections import defaultdict

from aocfw import AdventOfCodeClient

YEAR = 2018
DAY = 7


def parse_requirements(part_data):
    prerequisites = defaultdict(set)
    steps = set()

    for line in part_data.splitlines():
        before = line[5]
        after = line[36]
        steps.update((before, after))
        prerequisites[after].add(before)
        prerequisites[before]

    return steps, prerequisites


def available_steps(steps, prerequisites, completed, in_progress=None):
    if in_progress is None:
        in_progress = set()

    return sorted(
        step
        for step in steps
        if step not in completed
        and step not in in_progress
        and prerequisites[step] <= completed
    )


def part1(part_data):
    steps, prerequisites = parse_requirements(part_data)
    completed = set()
    order = []

    while len(completed) < len(steps):
        step = available_steps(steps, prerequisites, completed)[0]
        completed.add(step)
        order.append(step)

    return "".join(order)


def step_duration(step, base_duration):
    return base_duration + ord(step) - ord("A") + 1


def completion_time(part_data, worker_count, base_duration):
    steps, prerequisites = parse_requirements(part_data)
    completed = set()
    in_progress = {}
    elapsed = 0

    while len(completed) < len(steps):
        for step in available_steps(steps, prerequisites, completed, set(in_progress)):
            if len(in_progress) == worker_count:
                break
            in_progress[step] = step_duration(step, base_duration)

        elapsed += 1

        finished = []
        for step in list(in_progress):
            in_progress[step] -= 1
            if in_progress[step] == 0:
                finished.append(step)
                del in_progress[step]

        completed.update(finished)

    return elapsed


def part2(part_data):
    return completion_time(part_data, 5, 60)


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
