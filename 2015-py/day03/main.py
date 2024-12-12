with open("i.txt") as f:
    houses = {(0, 0): True}
    pos = (0,0)
    for line in f:
        for c in line:
            if c == 'v':
                pos = (pos[0], pos[1]+1)
            if c == '^':
                pos = (pos[0], pos[1] - 1)
            if c == '<':
                pos = (pos[0] - 1, pos[1])
            if c == '>':
                pos = (pos[0] + 1, pos[1])
            houses[pos] = True
    print(len(houses))


with open("i.txt") as f:
    houses = {(0, 0): True}
    posSanta = (0,0)
    posRobo = (0,0)
    pos = (0,0)
    santa = True
    for line in f:
        for c in line:
            if santa:
                pos = posSanta
            else:
                pos = posRobo
            if c == 'v':
                pos = (pos[0], pos[1]+1)
            if c == '^':
                pos = (pos[0], pos[1] - 1)
            if c == '<':
                pos = (pos[0] - 1, pos[1])
            if c == '>':
                pos = (pos[0] + 1, pos[1])
            houses[pos] = True
            if santa:
                posSanta = pos
            else:
                posRobo = pos
            santa = not santa
    print(len(houses))