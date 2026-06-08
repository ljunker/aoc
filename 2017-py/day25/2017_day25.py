import time
import re

from aocfw import AdventOfCodeClient

YEAR = 2017
DAY = 25


def parse_blueprint(part_data):
    start_state = re.search(r"Begin in state ([A-Z]).", part_data).group(1)
    steps = int(re.search(r"after (\d+) steps", part_data).group(1))
    states = {}

    for block in part_data.split("\n\n")[1:]:
        state = re.search(r"In state ([A-Z]):", block).group(1)
        states[state] = {}

        actions = re.findall(
            r"If the current value is ([01]):\n"
            r"\s+- Write the value ([01]).\n"
            r"\s+- Move one slot to the (left|right).\n"
            r"\s+- Continue with state ([A-Z]).",
            block,
        )

        for value, write, direction, next_state in actions:
            move = -1 if direction == "left" else 1
            states[state][int(value)] = (int(write), move, next_state)

    return start_state, steps, states


def diagnostic_checksum(part_data):
    state, steps, states = parse_blueprint(part_data)
    tape = set()
    cursor = 0

    for _ in range(steps):
        value = 1 if cursor in tape else 0
        write, move, state = states[state][value]

        if write:
            tape.add(cursor)
        else:
            tape.discard(cursor)

        cursor += move

    return len(tape)


def part1(part_data):
    return diagnostic_checksum(part_data)


def part2(part_data):
    return part1(part_data)


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
