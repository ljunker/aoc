import os
import re

from kryptikkaocutils.Input import write_input_to_file


def part1(inputs):
    w = 101
    h = 103
    seconds = 100
    pos = {}
    q0, q1, q2, q3 = 0,0,0,0
    for bot in inputs:
        x,y,vx,vy = bot[0], bot[1], bot[2], bot[3]
        x = (x + vx*seconds) % w
        y = (y + vy*seconds) % h
        if (x,y) not in pos:
            pos[(x, y)] = 1
        else:
            pos[(x, y)] += 1
    for x in range(w):
        if x == w // 2:
            continue
        for y in range(h):
            if y == h // 2:
                continue
            if (x,y) not in pos:
                continue
            v = pos[(x, y)]
            if x < w/2 and y < h/2:
                q0 += v
            elif x > w/2 and y < h/2:
                q1 += v
            elif x < w/2 and y > h/2:
                q2 += v
            elif x > w/2 and y > h/2:
                q3 += v
    print(q0* q1* q2* q3)


def displayBots(pos, w, h):
    for y in range(h):
        for x in range(w):
            if (x, y) not in pos:
                print(".", end='')
            else:
                print(pos[(x, y)], end='')
        print()
    print("==================================")

def part2(inputs):
    w = 101
    h = 103
    seconds = 100
    pos = {}
    for i in range(1000000):
        for bot in inputs:
            x, y, vx, vy = bot[0], bot[1], bot[2], bot[3]
            x = (x + vx * i) % w
            y = (y + vy * i) % h
            if (x, y) not in pos:
                pos[(x, y)] = 1
            else:
                pos[(x, y)] += 1
        if isOnlyOneInEveryCell(pos):
            print(i)
            displayBots(pos, w, h)
        #if isSymmetrical(pos, w, h):
        #    print(i)
        #    displayBots(pos, w, h)
        pos = {}


def isOnlyOneInEveryCell(pos):
    for _, value in pos.items():
        if value != 1:
            return False
    return True



def isSymmetrical(pos, w, h):
    symmetrical = True
    y = h // 2
    for x in range(w//2):
        antiX = w -1 -x
        if (x,y) not in pos and (antiX, y) in pos:
            return False
        else:
            if (antiX, y) not in pos:
                return False
            symmetrical = symmetrical and pos[(x, y)] == pos[(antiX, y)]
    return symmetrical

if __name__ == "__main__":
    fname = "i.txt"
    if not os.path.isfile(fname):
        write_input_to_file(2024, 14, fname)
    inputs = [[int(num) for num in re.findall(r"-?\d+", robot)] for robot in (open(fname).readlines())]
    part1(inputs)
    part2(inputs)