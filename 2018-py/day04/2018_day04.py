import time
import re
from collections import Counter, defaultdict

from aocfw import AdventOfCodeClient

YEAR = 2018
DAY = 4


def sleep_minutes(part_data):
    minutes_by_guard = defaultdict(Counter)
    guard = None
    asleep_at = None

    for line in sorted(part_data.splitlines()):
        minute = int(line[15:17])

        if "begins shift" in line:
            guard = int(re.search(r"#(\d+)", line).group(1))
        elif "falls asleep" in line:
            asleep_at = minute
        elif "wakes up" in line:
            minutes_by_guard[guard].update(range(asleep_at, minute))

    return minutes_by_guard


def part1(part_data):
    minutes_by_guard = sleep_minutes(part_data)
    guard, minutes = max(minutes_by_guard.items(), key=lambda item: sum(item[1].values()))
    minute, _ = minutes.most_common(1)[0]
    return guard * minute


def part2(part_data):
    minutes_by_guard = sleep_minutes(part_data)
    guard, minute, _ = max(
        (
            (guard, minute, count)
            for guard, minutes in minutes_by_guard.items()
            for minute, count in minutes.items()
        ),
        key=lambda item: item[2],
    )
    return guard * minute


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
