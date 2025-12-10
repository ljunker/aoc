from aocfw import AdventOfCodeClient, SubmissionStatus

YEAR = 2016
DAY = 3


def is_possible(triangle):
    return 1 if (triangle[0] + triangle[1] > triangle[2]
            and triangle[0] + triangle[2] > triangle[1]
            and triangle[1] + triangle[2] > triangle[0]) else 0

def part1(part_data):
    triangles = [
        [
            int(x.strip())
            for x in line.strip().split()
        ]
        for line in part_data.split("\n")
    ]
    return sum([is_possible(triangle) for triangle in triangles])


def part2(part_data):
    grid = []
    triangles = []
    for y, line in enumerate(part_data.split("\n")):
        grid.append([])
        for x, num in enumerate(line.strip().split()):
            grid[y].append(int(num))
    for x in range(3):
        y = 0
        for _ in range(len(grid)):
            if y == len(grid):
                break
            triangles.append([grid[y][x], grid[y+1][x], grid[y+2][x]])
            y += 3
    return sum([is_possible(triangle) for triangle in triangles])


if __name__ == "__main__":
    client = AdventOfCodeClient()

    data = client.get_input(YEAR, DAY)
    answer = part1(data)
    print("Part 1:", answer)
    # res = client.submit_answer(YEAR, DAY, 1, answer)
    # print(res.message)

    answer = part2(data)
    print("Part 2:", answer)
    res = client.submit_answer(YEAR, DAY, 2, answer)
    print(res.message)
