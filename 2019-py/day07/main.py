import copy
from itertools import permutations

from IntComputer.computer import IntComputer

original_program = [int(num) for num in open("program.txt").read().split(",")]

settings = [0,1,2,3,4]
perms = list(permutations(settings))
max_signal = 0
for p in perms:
    s = list(p)
    c = IntComputer(copy.deepcopy(original_program), True, True)
    c.run_program()
    c.piped_input = [s.pop(0), 0]
    c.run_program()
    [out] = c.get_output()
    for setting in s:
        c = IntComputer(copy.deepcopy(original_program), True, True)
        c.run_program()
        c.piped_input = [setting, out]
        c.run_program()
        [out] = c.get_output()
    if max_signal < out:
        max_signal = out
print(max_signal)

c = IntComputer(copy.deepcopy(original_program), True, True)
c.piped_input = [9, 18216]
c.run_program()

settings = [5,6,7,8,9]
perms = list(permutations(settings))
max_signal = 0

signals = []

for p in perms:
    computers = []
    s = list(p)
    for setting in s:
        original_program = [int(num) for num in open("program.txt").read().split(",")]
        computer = IntComputer(original_program, True, True)
        computer.piped_input = [setting]
        computers.append(computer)
    input = 0
    current = 0
    while True:
        c = computers[current]
        current += 1
        current %= 5
        c.piped_input.append(input)
        finished = c.run_program()
        input = c.get_output().pop(0)
        if finished and c == computers[4]:
            signals.append(input)
            break
print(max(signals))