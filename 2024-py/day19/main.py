from kryptikkaocutils.Timer import timer


def can_create_design(available_towels, design):
    n = len(design)
    dp = [False] * (n + 1)
    dp[0] = True

    for i in range(n):
        if not dp[i]:
            continue
        for towel in available_towels:
            if design[i:i + len(towel)] == towel:
                dp[i + len(towel)] = True

    return dp[n]


def count_design_ways(available_towels, design):
    n = len(design)
    dp = [0] * (n + 1)
    dp[0] = 1

    for i in range(n):
        if dp[i] == 0:
            continue
        for towel in available_towels:
            if design[i:i + len(towel)] == towel:
                dp[i + len(towel)] += dp[i]

    return dp[n]


@timer
def part1():
    print(sum([1 for d in designs if can_create_design(available_towels, d)]))


@timer
def part2():
    print(sum([count_design_ways(available_towels, design) for design in designs]))


if __name__ == "__main__":
    f = open("i.txt")
    available_towels, designs = f.read().split("\n\n")
    available_towels = [t.strip() for t in available_towels.split(",")]
    designs = [d.strip() for d in designs.split("\n")]
    part1()
    part2()
