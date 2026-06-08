import time
import re

from aocfw import AdventOfCodeClient

YEAR = 2018
DAY = 16


def part1(part_data):
    samples, _ = parse_input(part_data)
    return sum(1 for sample in samples if len(matching_ops(sample)) >= 3)


def part2(part_data):
    samples, program = parse_input(part_data)
    mapping = resolve_mapping(samples)
    registers = [0, 0, 0, 0]

    for opcode, a, b, c in program:
        registers = apply_op(mapping[opcode], registers, a, b, c)

    return registers[0]


def parse_input(part_data):
    sample_data, _, program_data = part_data.rstrip().partition("\n\n\n\n")
    samples = []

    for before, instruction, after in re.findall(
        r"Before: \[(.*?)\]\n(.*?)\nAfter:  \[(.*?)\]",
        sample_data,
    ):
        samples.append((
            parse_numbers(before),
            parse_numbers(instruction),
            parse_numbers(after),
        ))

    program = [
        parse_numbers(line)
        for line in program_data.splitlines()
        if line
    ]
    return samples, program


def parse_numbers(text):
    return [int(number) for number in re.findall(r"\d+", text)]


def apply_op(name, registers, a, b, c):
    result = registers.copy()

    if name == "addr":
        result[c] = registers[a] + registers[b]
    elif name == "addi":
        result[c] = registers[a] + b
    elif name == "mulr":
        result[c] = registers[a] * registers[b]
    elif name == "muli":
        result[c] = registers[a] * b
    elif name == "banr":
        result[c] = registers[a] & registers[b]
    elif name == "bani":
        result[c] = registers[a] & b
    elif name == "borr":
        result[c] = registers[a] | registers[b]
    elif name == "bori":
        result[c] = registers[a] | b
    elif name == "setr":
        result[c] = registers[a]
    elif name == "seti":
        result[c] = a
    elif name == "gtir":
        result[c] = 1 if a > registers[b] else 0
    elif name == "gtri":
        result[c] = 1 if registers[a] > b else 0
    elif name == "gtrr":
        result[c] = 1 if registers[a] > registers[b] else 0
    elif name == "eqir":
        result[c] = 1 if a == registers[b] else 0
    elif name == "eqri":
        result[c] = 1 if registers[a] == b else 0
    elif name == "eqrr":
        result[c] = 1 if registers[a] == registers[b] else 0
    else:
        raise ValueError(name)

    return result


def matching_ops(sample):
    before, instruction, after = sample
    _, a, b, c = instruction
    return {
        name
        for name in OPS
        if apply_op(name, before, a, b, c) == after
    }


def resolve_mapping(samples):
    candidates = {
        opcode: set(OPS)
        for opcode in range(16)
    }

    for sample in samples:
        opcode = sample[1][0]
        candidates[opcode] &= matching_ops(sample)

    resolved = {}
    while len(resolved) < len(candidates):
        singles = [
            (opcode, next(iter(names)))
            for opcode, names in candidates.items()
            if opcode not in resolved and len(names) == 1
        ]

        if not singles:
            raise ValueError(f"Unresolved opcodes: {candidates}")

        for opcode, name in singles:
            resolved[opcode] = name
            for other_opcode, other_names in candidates.items():
                if other_opcode != opcode:
                    other_names.discard(name)

    return resolved


OPS = (
    "addr",
    "addi",
    "mulr",
    "muli",
    "banr",
    "bani",
    "borr",
    "bori",
    "setr",
    "seti",
    "gtir",
    "gtri",
    "gtrr",
    "eqir",
    "eqri",
    "eqrr",
)


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
