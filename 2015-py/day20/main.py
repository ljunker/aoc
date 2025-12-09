def solve_part1(target):
    # Upper bound: the first solution will be <= target // 10 (safe enough).
    limit = target // 10
    presents = [0] * (limit + 1)

    for elf in range(1, limit + 1):
        gift = 10 * elf
        for house in range(elf, limit + 1, elf):
            presents[house] += gift

    for house in range(1, limit + 1):
        if presents[house] >= target:
            return house

    return None


def solve_part2(target):
    # With 11 * elf and 50-house limit, this bound works fine:
    limit = target // 11
    presents = [0] * (limit + 1)

    for elf in range(1, limit + 1):
        gift = 11 * elf
        max_house = min(limit, elf * 50)
        for house in range(elf, max_house + 1, elf):
            presents[house] += gift

    for house in range(1, limit + 1):
        if presents[house] >= target:
            return house

    return None


if __name__ == "__main__":
    with open("i.txt") as f:
        target = int(f.read().strip())

    part1 = solve_part1(target)
    print("Part 1 - first house with enough presents:", part1)

    part2 = solve_part2(target)
    print("Part 2 - first house with enough presents (11x, 50 houses):", part2)
