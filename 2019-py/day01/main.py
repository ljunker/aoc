from kryptikkaocutils.Timer import timer


def calc_fuel(m):
    fuel = m // 3 - 2
    if (fuel < 0):
        return 0
    return fuel


@timer
def part1():
    with open("i.txt") as f:
        masses = [int(num) for num in f.readlines()]
        fuels = [calc_fuel(m) for m in masses]
        s = sum(fuels)
        print(s)


@timer
def part2():
    with open("i.txt") as f:
        masses = [int(num) for num in f.readlines()]
        fuels = [calc_fuel(m) for m in masses]
        s = sum(fuels)
        f = s
        while f > 0:
            fuels = [calc_fuel(m) for m in fuels]
            s += sum(fuels)
            f = sum(fuels)
        print(s)


part1()
part2()
