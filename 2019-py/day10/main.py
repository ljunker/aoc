import math

from kryptikkaocutils.Timer import timer


def init_asteroids():
    with open('i.txt') as f:
        for y, line in enumerate(f.readlines()):
            for x, a in enumerate(line):
                if a == '#':
                    yield (x, y)


asteroids = list(init_asteroids())


def angle(start, end):
    result = math.atan2(end[0] - start[0], start[1] - end[1]) * 180 / math.pi
    if result < 0:
        return 360 + result
    return result


@timer
def part1():
    result = None
    m = 0

    for start in asteroids:
        cnt = len({angle(start, end) for end in asteroids if start != end})
        if cnt > m:
            m = cnt
            result = start

    print('x {} y {}'.format(*result))
    print('visible {}'.format(m))
    return result


@timer
def part2(station):
    asteroids.remove(station)
    angles = sorted(
        ((angle(station, end), end) for end in asteroids),
        key=lambda x: (x[0], abs(station[0] - x[1][0]) + abs(station[1] - x[1][1]))
    )

    idx = 0
    last = angles.pop(idx)
    last_angle = last[0]
    cnt = 1

    while cnt < 200 and angles:
        if idx >= len(angles):
            idx = 0
            last_angle = None
        if last_angle == angles[idx][0]:
            idx += 1
            continue
        last = angles.pop(idx)
        last_angle = last[0]
        cnt += 1
    print('vaporized {}: {} {}'.format(cnt, last[1], last[1][0] * 100 + last[1][1]))


if __name__ == '__main__':
    station = part1()
    part2(station)
