import time

from aocfw import AdventOfCodeClient

YEAR = 2017
DAY = 16


def parse_moves(part_data):
    return part_data.strip().split(",")


def dance(moves, programs):
    programs = list(programs)

    for move in moves:
        kind = move[0]

        if kind == "s":
            amount = int(move[1:])
            programs = programs[-amount:] + programs[:-amount]
        elif kind == "x":
            left, right = [int(value) for value in move[1:].split("/")]
            programs[left], programs[right] = programs[right], programs[left]
        elif kind == "p":
            left_name, right_name = move[1:].split("/")
            left = programs.index(left_name)
            right = programs.index(right_name)
            programs[left], programs[right] = programs[right], programs[left]

    return "".join(programs)


def repeat_dance(moves, programs, rounds):
    seen = {}
    order = programs
    round_number = 0

    while round_number < rounds:
        if order in seen:
            cycle_length = round_number - seen[order]
            remaining = (rounds - round_number) % cycle_length
            for _ in range(remaining):
                order = dance(moves, order)
            return order

        seen[order] = round_number
        order = dance(moves, order)
        round_number += 1

    return order


def part1(part_data):
    return dance(parse_moves(part_data), "abcdefghijklmnop")


def part2(part_data):
    return repeat_dance(parse_moves(part_data), "abcdefghijklmnop", 1_000_000_000)


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
