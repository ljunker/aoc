import re

from kryptikkaocutils.Timer import timer


@timer
def part2(wires):
    crossings = set(wires[0]) & set(wires[1])
    nearest = sorted(crossings, key=lambda c: wires[0].index(c) + wires[1].index(c))[0]
    print(wires[0].index(nearest) + wires[1].index(nearest) + 2)

@timer
def part1(wires):
    crossings = set(wires[0]) & set(wires[1])
    print(min([abs(c[0]) + abs(c[1])for c in crossings]))

directions = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, -1),
    'D': (0, 1)
}

def ch_to_d(ch):
    return directions[ch]

def add(t1, t2):
    return tuple(map(sum, zip(t1, t2)))

input = open("i.txt").readlines()
wires = []
for l in input:
    current = (0,0)
    wire = []
    for instr in l.split(","):
        match = re.search(r"(.*?)(\d+)", instr)
        d, a = ch_to_d(match.group(1)), int(match.group(2))
        for i in range(a):
            current = add(current, d)
            wire.append(current)
    wires.append(wire)
#print(wires)
part1(wires)
part2(wires)