import time
from collections import defaultdict, deque

from aocfw import AdventOfCodeClient

YEAR = 2016
DAY = 10


def parse(part_data):
    bots = defaultdict(list)
    rules = {}

    for line in part_data.splitlines():
        parts = line.split()
        if parts[0] == "value":
            value = int(parts[1])
            bot = int(parts[-1])
            bots[bot].append(value)
        elif parts[0] == "bot":
            bot = int(parts[1])
            rules[bot] = (
                (parts[5], int(parts[6])),
                (parts[10], int(parts[11])),
            )
        else:
            raise ValueError(f"Unknown instruction: {line}")

    return bots, rules


def simulate(part_data, watched=(17, 61)):
    bots, rules = parse(part_data)
    outputs = defaultdict(list)
    ready = deque(bot for bot, chips in bots.items() if len(chips) == 2)
    watched_bot = None
    watched = sorted(watched)

    while ready:
        bot = ready.popleft()
        if len(bots[bot]) < 2:
            continue

        low, high = sorted(bots[bot])
        bots[bot].clear()

        if [low, high] == watched:
            watched_bot = bot

        for value, target in zip((low, high), rules[bot]):
            target_type, target_id = target
            if target_type == "bot":
                bots[target_id].append(value)
                if len(bots[target_id]) == 2:
                    ready.append(target_id)
            elif target_type == "output":
                outputs[target_id].append(value)
            else:
                raise ValueError(f"Unknown target type: {target_type}")

    return watched_bot, outputs


def part1(part_data):
    watched_bot, _ = simulate(part_data)
    return watched_bot


def part2(part_data):
    _, outputs = simulate(part_data)
    return outputs[0][0] * outputs[1][0] * outputs[2][0]


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
