import time

from aocfw import AdventOfCodeClient

YEAR = 2016
DAY = 23
REGISTERS = "abcd"


def value(registers, arg):
    if arg.lstrip("-").isdigit():
        return int(arg)
    return registers[arg]


def toggle(instruction):
    if len(instruction) == 2:
        return ["dec", instruction[1]] if instruction[0] == "inc" else ["inc", instruction[1]]
    if len(instruction) == 3:
        return ["cpy", instruction[1], instruction[2]] if instruction[0] == "jnz" else ["jnz", instruction[1], instruction[2]]

    raise ValueError(f"Cannot toggle instruction: {' '.join(instruction)}")


def optimize_multiply(instructions, registers, pointer):
    if pointer + 5 >= len(instructions):
        return False

    window = instructions[pointer:pointer + 6]
    if (
        len(window[0]) == 3
        and len(window[1]) == 2
        and len(window[2]) == 2
        and len(window[3]) == 3
        and len(window[4]) == 2
        and len(window[5]) == 3
        and window[0][0] == "cpy"
        and window[1][0] == "inc"
        and window[2][0] == "dec"
        and window[3] == ["jnz", window[2][1], "-2"]
        and window[4][0] == "dec"
        and window[5] == ["jnz", window[4][1], "-5"]
        and window[0][2] == window[2][1]
        and window[1][1] in REGISTERS
        and window[2][1] in REGISTERS
        and window[4][1] in REGISTERS
    ):
        registers[window[1][1]] += value(registers, window[0][1]) * registers[window[4][1]]
        registers[window[2][1]] = 0
        registers[window[4][1]] = 0
        return True

    return False


def run_program(part_data, a=0):
    instructions = [line.split() for line in part_data.splitlines() if line.strip()]
    registers = {reg: 0 for reg in REGISTERS}
    registers["a"] = a
    pointer = 0

    while 0 <= pointer < len(instructions):
        if optimize_multiply(instructions, registers, pointer):
            pointer += 6
            continue

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
        elif op == "tgl":
            target = pointer + value(registers, instruction[1])
            if 0 <= target < len(instructions):
                instructions[target] = toggle(instructions[target])
            pointer += 1
        else:
            raise ValueError(f"Unknown instruction: {' '.join(instruction)}")

    return registers


def part1(part_data):
    return run_program(part_data, a=7)["a"]


def part2(part_data):
    return run_program(part_data, a=12)["a"]


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
