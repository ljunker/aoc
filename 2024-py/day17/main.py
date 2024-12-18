import copy

from kryptikkaocutils.Timer import timer


def combo(num, registers):
    if num <= 3:
        return num
    elif num == 4:
        return registers['A']
    elif num == 5:
        return registers['B']
    elif num == 6:
        return registers['C']


def adv(num, registers, instr, outputs):
    registers['A'] = registers['A'] // (2 ** combo(num, registers))
    return registers, instr + 2, outputs


def bxl(num, registers, instr, outputs):
    registers['B'] = registers['B'] ^ num
    return registers, instr + 2, outputs


def bst(num, registers, instr, outputs):
    registers['B'] = combo(num, registers) % 8
    return registers, instr + 2, outputs


def jnz(num, registers, instr, outputs):
    if registers['A'] == 0:
        return registers, instr + 2, outputs
    else:
        return registers, num, outputs


def bxc(num, registers, instr, outputs):
    registers['B'] = registers['B'] ^ registers['C']
    return registers, instr + 2, outputs


def out(num, registers, instr, outputs):
    outputs.append(combo(num, registers) % 8)
    return registers, instr + 2, outputs


def bdv(num, registers, instr, outputs):
    registers['B'] = registers['A'] // (2 ** combo(num, registers))
    return registers, instr + 2, outputs


def cdv(num, registers, instr, outputs):
    registers['C'] = registers['A'] // (2 ** combo(num, registers))
    return registers, instr + 2, outputs


@timer
def part1(registers, program):
    outputs = []
    length = len(program)
    instr = 0
    while instr in range(length):
        opcode = program[instr]
        function = [adv, bxl, bst, jnz, bxc, out, bdv, cdv][opcode]
        num = program[instr + 1]
        registers, instr, outputs = function(num, registers, instr, outputs)

    answer = ','.join(str(num) for num in outputs)
    print(answer)


def get_output(a, registers_original):
    outputs = []
    registers = copy.deepcopy(registers_original)
    registers['A'] = a
    length = len(program)
    instr = 0
    while instr in range(length):
        opcode = program[instr]
        function = [adv, bxl, bst, jnz, bxc, out, bdv, cdv][opcode]
        num = program[instr + 1]
        registers, instr, outputs = function(num, registers, instr, outputs)
    return outputs


@timer
def part2(register_orig, programs):
    A = 0
    for n in range(1, len(programs)+1):
        A = A<<3
        i = 0
        while True:
            newA = A + i
            if get_output(newA, register_orig) == programs[-n:]:
                A = newA
                break
            i += 1
    print(A)


if __name__ == "__main__":
    with open('i.txt') as f:
        registers, program = f.read().split('\n\n')

    registers = {line.split(': ')[0].split()[1]: int(line.split(': ')[1]) for line in registers.splitlines()}
    registers_orig = copy.deepcopy(registers)
    program = [int(num) for num in program.replace('\n', '').split()[1].split(',')]
    part1(registers, program)
    part2(registers_orig, program)
