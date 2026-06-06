import time
import re
from collections import deque
from dataclasses import dataclass

from aocfw import AdventOfCodeClient

YEAR = 2016
DAY = 22
NODE_RE = re.compile(
    r"node-x(?P<x>\d+)-y(?P<y>\d+)\s+"
    r"(?P<size>\d+)T\s+"
    r"(?P<used>\d+)T\s+"
    r"(?P<avail>\d+)T"
)


@dataclass(frozen=True)
class Node:
    x: int
    y: int
    size: int
    used: int
    avail: int


def parse_nodes(part_data):
    nodes = []
    for line in part_data.splitlines():
        match = NODE_RE.search(line)
        if match:
            nodes.append(Node(**{key: int(value) for key, value in match.groupdict().items()}))

    return nodes


def count_viable_pairs(nodes):
    return sum(
        1
        for source in nodes
        for target in nodes
        if source != target and source.used > 0 and source.used <= target.avail
    )


def neighbors(position):
    x, y = position
    yield x - 1, y
    yield x + 1, y
    yield x, y - 1
    yield x, y + 1


def minimum_steps_to_goal(nodes):
    grid = {(node.x, node.y): node for node in nodes}
    empty = next(node for node in nodes if node.used == 0)
    empty_position = (empty.x, empty.y)
    goal_position = (max(node.x for node in nodes), 0)
    passable = {
        position
        for position, node in grid.items()
        if node.used <= empty.size
    }

    queue = deque([((empty_position, goal_position), 0)])
    seen = {(empty_position, goal_position)}

    while queue:
        (current_empty, current_goal), steps = queue.popleft()
        if current_goal == (0, 0):
            return steps

        for next_empty in neighbors(current_empty):
            if next_empty not in passable:
                continue

            next_goal = current_empty if next_empty == current_goal else current_goal
            state = (next_empty, next_goal)
            if state not in seen:
                seen.add(state)
                queue.append((state, steps + 1))

    raise ValueError("Goal data cannot be moved to x0-y0")


def part1(part_data):
    return count_viable_pairs(parse_nodes(part_data))


def part2(part_data):
    return minimum_steps_to_goal(parse_nodes(part_data))


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
