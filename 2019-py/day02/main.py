import copy

from kryptikkaocutils.Timer import timer


def run_program(program):
    instr = 0
    op = 0
    while op != 99:
        op = program[instr]
        if op == 1:
            pos = [program[instr + 1], program[instr + 2], program[instr + 3]]
            program[pos[2]] = program[pos[0]] + program[pos[1]]
            instr += 4
        elif op == 2:
            pos = [program[instr + 1], program[instr + 2], program[instr + 3]]
            program[pos[2]] = program[pos[0]] * program[pos[1]]
            instr += 4
    return program[0]


@timer
def part1():
    f = open("i.txt")
    program = [int(num) for num in f.read().split(",")]
    program[1] = 12
    program[2] = 2
    result = run_program(program)
    print(result)

@timer
def part2():
    f = open("i.txt")
    program_original = [int(num) for num in f.read().split(",")]

    for verb in range(100):
        for noun in range(100):
            program = copy.deepcopy(program_original)
            program[1] = noun
            program[2] = verb
            result = run_program(program)
            if result == 19690720:
                print(noun*100 + verb)


part1()
part2()
