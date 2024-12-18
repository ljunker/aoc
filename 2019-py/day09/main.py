from IntComputer.computer import IntComputer

if __name__ == "__main__":
    program = [int(num) for num in open("program.txt").read().split(",")]

    c = IntComputer(program, False, False)
    c.run_program()