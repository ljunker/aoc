from aocfw import AdventOfCodeClient

YEAR = 2025
DAY = 12


def part1(text: str) -> int:
    chunks = text.replace(":", "").replace("x", " ").split("\n\n")
    regions = chunks.pop()
    areas = [x.count("#") for x in chunks]
    a = 0
    for line in regions.splitlines():
        w, h, *counts = map(int, line.split())
        area_needed = sum(areas[i] * x for i, x in enumerate(counts))
        a += area_needed <= w * h
    return a


if __name__ == "__main__":
    client = AdventOfCodeClient()

    data = client.get_input(YEAR, DAY)
    answer = part1(data)
    print("Part 1:", answer)
    # res = client.submit_answer(YEAR, DAY, 1, answer)
    # print(res.message)
