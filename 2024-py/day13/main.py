import re
from sympy import solve, Symbol


def play(ax, ay, bx, by, px, py):
    a = Symbol("a", integer=True)
    b = Symbol("b", integer=True)
    px += 10000000000000
    py += 10000000000000
    roots = solve(
        [a * ax + b * bx - px, a * ay + b * by - py],
        [a, b],
    )
    if roots:
        return roots[a] * 3 + roots[b]
    else:
        return 0


s = 0
inputs = [[int(num) for num in re.findall(r"\d+", machine)] for machine in (open("i.txt").read().split("\n\n"))]
for e in inputs:
    s += play(*e)
print(s)
