def load_program(filename="i.txt"):
    prog = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            prog.append(line)
    return prog


def run(prog, a_start=0, b_start=0):
    regs = {"a": a_start, "b": b_start}
    ip = 0  # instruction pointer

    while 0 <= ip < len(prog):
        inst = prog[ip].split()

        op = inst[0]

        if op == "hlf":
            r = inst[1]
            regs[r] //= 2
            ip += 1

        elif op == "tpl":
            r = inst[1]
            regs[r] *= 3
            ip += 1

        elif op == "inc":
            r = inst[1]
            regs[r] += 1
            ip += 1

        elif op == "jmp":
            offset = int(inst[1])
            ip += offset

        elif op == "jie":
            # form: "jie a, +2"
            r = inst[1].rstrip(",")
            offset = int(inst[2])
            if regs[r] % 2 == 0:
                ip += offset
            else:
                ip += 1

        elif op == "jio":
            # form: "jio a, +2"
            r = inst[1].rstrip(",")
            offset = int(inst[2])
            if regs[r] == 1:
                ip += offset
            else:
                ip += 1

        else:
            raise ValueError(f"Unknown instruction: {prog[ip]}")

    return regs


if __name__ == "__main__":
    program = load_program("i.txt")

    # Part 1: a = 0, b = 0
    regs1 = run(program, a_start=0, b_start=0)
    print("Part 1 - register b:", regs1["b"])

    # Part 2 (AoC twist): a = 1, b = 0
    regs2 = run(program, a_start=1, b_start=0)
    print("Part 2 - register b:", regs2["b"])
