import time

from aocfw import AdventOfCodeClient

YEAR = 2018
DAY = 14


def part1(part_data):
    return scores_after(int(part_data), 10)


def part2(part_data):
    return recipes_before(part_data.strip())


def append_scores(recipes, elf1, elf2):
    total = recipes[elf1] + recipes[elf2]
    if total >= 10:
        recipes.append(total // 10)
    recipes.append(total % 10)
    elf1 = (elf1 + recipes[elf1] + 1) % len(recipes)
    elf2 = (elf2 + recipes[elf2] + 1) % len(recipes)
    return elf1, elf2


def scores_after(offset, count):
    recipes = [3, 7]
    elf1 = 0
    elf2 = 1

    while len(recipes) < offset + count:
        elf1, elf2 = append_scores(recipes, elf1, elf2)

    return "".join(str(score) for score in recipes[offset:offset + count])


def recipes_before(pattern):
    target = [int(char) for char in pattern]
    target_length = len(target)
    recipes = [3, 7]
    elf1 = 0
    elf2 = 1

    while True:
        previous_length = len(recipes)
        elf1, elf2 = append_scores(recipes, elf1, elf2)

        for index in range(previous_length, len(recipes)):
            start = index - target_length + 1
            if start >= 0 and recipes[start:index + 1] == target:
                return start


if __name__ == "__main__":
    client = AdventOfCodeClient()

    data = client.get_input(YEAR, DAY)
    answer = part1(data)
    print("Part 1:", answer)
    res = client.submit_answer(YEAR, DAY, 1, answer)
    print(res.message)

    time.sleep(10)

    answer = part2(data)
    print("Part 2:", answer)
    res = client.submit_answer(YEAR, DAY, 2, answer)
    print(res.message)
