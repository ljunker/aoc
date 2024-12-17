import copy

from kryptikkaocutils.Timer import timer

from IntComputer.computer import IntComputer


@timer
def part1():
    f = open("i.txt")
    program = [int(num) for num in f.read().split(",")]
    program[1] = 12
    program[2] = 2
    c = IntComputer(program)
    c.run_program()
    print(c.result())


@timer
def part2():
    f = open("i.txt")
    program_original = [int(num) for num in f.read().split(",")]

    for verb in range(100):
        for noun in range(100):
            program = copy.deepcopy(program_original)
            program[1] = noun
            program[2] = verb
            c = IntComputer(program)
            c.run_program()
            result = c.result()
            if result == 19690720:
                print(noun * 100 + verb)


part1()
part2()
