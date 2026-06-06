import time

from aocfw import AdventOfCodeClient

YEAR = 2016
DAY = 25
REGISTERS = "abcd"
SIGNAL_LENGTH = 20


def value(registers, arg):
    if arg.lstrip("-").isdigit():
        return int(arg)
    return registers[arg]


def run_program(part_data, a=0, max_outputs=SIGNAL_LENGTH):
    instructions = [line.split() for line in part_data.splitlines() if line.strip()]
    registers = {reg: 0 for reg in REGISTERS}
    registers["a"] = a
    pointer = 0
    outputs = []

    while 0 <= pointer < len(instructions) and len(outputs) < max_outputs:
        instruction = instructions[pointer]
        op = instruction[0]

        if op == "cpy":
            if instruction[2] in REGISTERS:
                registers[instruction[2]] = value(registers, instruction[1])
            pointer += 1
        elif op == "inc":
            if instruction[1] in REGISTERS:
                registers[instruction[1]] += 1
            pointer += 1
        elif op == "dec":
            if instruction[1] in REGISTERS:
                registers[instruction[1]] -= 1
            pointer += 1
        elif op == "jnz":
            if value(registers, instruction[1]) != 0:
                pointer += value(registers, instruction[2])
            else:
                pointer += 1
        elif op == "out":
            outputs.append(value(registers, instruction[1]))
            pointer += 1
        else:
            raise ValueError(f"Unknown instruction: {' '.join(instruction)}")

    return outputs


def is_clock_signal(outputs):
    return all(output == index % 2 for index, output in enumerate(outputs))


def find_initial_value(part_data):
    initial_value = 1
    while True:
        outputs = run_program(part_data, a=initial_value)
        if len(outputs) == SIGNAL_LENGTH and is_clock_signal(outputs):
            return initial_value

        initial_value += 1


def part1(part_data):
    return find_initial_value(part_data)


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
