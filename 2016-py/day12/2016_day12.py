import time

from aocfw import AdventOfCodeClient

YEAR = 2016
DAY = 12


def value(registers, arg):
    if arg.lstrip("-").isdigit():
        return int(arg)
    return registers[arg]


def run_program(part_data, c=0):
    instructions = [line.split() for line in part_data.splitlines()]
    registers = {reg: 0 for reg in "abcd"}
    registers["c"] = c
    pointer = 0

    while 0 <= pointer < len(instructions):
        instruction = instructions[pointer]
        op = instruction[0]

        if op == "cpy":
            registers[instruction[2]] = value(registers, instruction[1])
            pointer += 1
        elif op == "inc":
            registers[instruction[1]] += 1
            pointer += 1
        elif op == "dec":
            registers[instruction[1]] -= 1
            pointer += 1
        elif op == "jnz":
            if value(registers, instruction[1]) != 0:
                pointer += value(registers, instruction[2])
            else:
                pointer += 1
        else:
            raise ValueError(f"Unknown instruction: {' '.join(instruction)}")

    return registers


def part1(part_data):
    return run_program(part_data)["a"]


def part2(part_data):
    return run_program(part_data, c=1)["a"]


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
