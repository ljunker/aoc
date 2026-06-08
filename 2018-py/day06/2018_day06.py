import time

from aocfw import AdventOfCodeClient

YEAR = 2018
DAY = 6


def parse_points(part_data):
    points = []

    for line in part_data.splitlines():
        x, y = line.split(", ")
        points.append((int(x), int(y)))

    return points


def distance(left, right):
    return abs(left[0] - right[0]) + abs(left[1] - right[1])


def bounds(points):
    xs = [x for x, _ in points]
    ys = [y for _, y in points]
    return min(xs), max(xs), min(ys), max(ys)


def closest_point(point, points):
    distances = [(distance(point, other), index) for index, other in enumerate(points)]
    distances.sort()

    if distances[0][0] == distances[1][0]:
        return None

    return distances[0][1]


def part1(part_data):
    points = parse_points(part_data)
    min_x, max_x, min_y, max_y = bounds(points)
    areas = [0] * len(points)
    infinite = set()

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            closest = closest_point((x, y), points)
            if closest is None:
                continue

            areas[closest] += 1
            if x in (min_x, max_x) or y in (min_y, max_y):
                infinite.add(closest)

    return max(area for index, area in enumerate(areas) if index not in infinite)


def safe_region_size(part_data, limit):
    points = parse_points(part_data)
    min_x, max_x, min_y, max_y = bounds(points)
    margin = limit // len(points) + 1
    safe = 0

    for x in range(min_x - margin, max_x + margin + 1):
        for y in range(min_y - margin, max_y + margin + 1):
            if sum(distance((x, y), point) for point in points) < limit:
                safe += 1

    return safe


def part2(part_data):
    return safe_region_size(part_data, 10_000)


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
