import time
from collections import defaultdict, deque

from aocfw import AdventOfCodeClient

YEAR = 2017
DAY = 18


def parse_instructions(part_data):
    return [line.split() for line in part_data.splitlines()]


def value(registers, token):
    try:
        return int(token)
    except ValueError:
        return registers[token]


def part1(part_data):
    instructions = parse_instructions(part_data)
    registers = defaultdict(int)
    last_sound = None
    index = 0

    while 0 <= index < len(instructions):
        instruction = instructions[index]
        operation = instruction[0]

        if operation == "snd":
            last_sound = value(registers, instruction[1])
        elif operation == "set":
            registers[instruction[1]] = value(registers, instruction[2])
        elif operation == "add":
            registers[instruction[1]] += value(registers, instruction[2])
        elif operation == "mul":
            registers[instruction[1]] *= value(registers, instruction[2])
        elif operation == "mod":
            registers[instruction[1]] %= value(registers, instruction[2])
        elif operation == "rcv" and value(registers, instruction[1]):
            return last_sound
        elif operation == "jgz" and value(registers, instruction[1]) > 0:
            index += value(registers, instruction[2])
            continue

        index += 1

    return last_sound


def run_until_wait(instructions, registers, queue, other_queue, index):
    sent = 0

    while 0 <= index < len(instructions):
        instruction = instructions[index]
        operation = instruction[0]

        if operation == "snd":
            other_queue.append(value(registers, instruction[1]))
            sent += 1
        elif operation == "set":
            registers[instruction[1]] = value(registers, instruction[2])
        elif operation == "add":
            registers[instruction[1]] += value(registers, instruction[2])
        elif operation == "mul":
            registers[instruction[1]] *= value(registers, instruction[2])
        elif operation == "mod":
            registers[instruction[1]] %= value(registers, instruction[2])
        elif operation == "rcv":
            if not queue:
                return index, sent, False
            registers[instruction[1]] = queue.popleft()
        elif operation == "jgz" and value(registers, instruction[1]) > 0:
            index += value(registers, instruction[2])
            continue

        index += 1

    return index, sent, True


def part2(part_data):
    instructions = parse_instructions(part_data)
    registers = [defaultdict(int), defaultdict(int)]
    registers[0]["p"] = 0
    registers[1]["p"] = 1
    queues = [deque(), deque()]
    indexes = [0, 0]
    terminated = [False, False]
    program_1_sends = 0

    while True:
        made_progress = False

        for program in range(2):
            if terminated[program]:
                continue

            old_index = indexes[program]
            old_queue_size = len(queues[program])
            indexes[program], sent, terminated[program] = run_until_wait(
                instructions,
                registers[program],
                queues[program],
                queues[1 - program],
                indexes[program],
            )
            if program == 1:
                program_1_sends += sent

            made_progress = (
                made_progress
                or sent > 0
                or indexes[program] != old_index
                or len(queues[program]) != old_queue_size
            )

        if not made_progress:
            return program_1_sends


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
