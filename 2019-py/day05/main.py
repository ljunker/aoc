from kryptikkaocutils.Timer import timer

from IntComputer.computer import IntComputer


@timer
def part1():
    f = open("i.txt")
    program = [int(num) for num in f.read().split(",")]
    c = IntComputer(program)
    c.run_program()
    print(c.result())


if __name__ == "__main__":
    part1()
