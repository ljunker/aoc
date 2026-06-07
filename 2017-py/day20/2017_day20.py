import time
import re
from collections import defaultdict
from math import isqrt

from aocfw import AdventOfCodeClient

YEAR = 2017
DAY = 20


def parse_particles(part_data):
    particles = []

    for line in part_data.splitlines():
        values = [int(value) for value in re.findall(r"-?\d+", line)]
        particles.append(
            (tuple(values[:3]), tuple(values[3:6]), tuple(values[6:9]))
        )

    return particles


def manhattan(vector):
    return sum(abs(value) for value in vector)


def position_at(particle, tick):
    position, velocity, acceleration = particle

    return tuple(
        position[axis]
        + velocity[axis] * tick
        + acceleration[axis] * tick * (tick + 1) // 2
        for axis in range(3)
    )


def matching_times_for_axis(left, right, axis):
    p1, v1, a1 = left
    p2, v2, a2 = right
    acceleration = a1[axis] - a2[axis]
    velocity = 2 * (v1[axis] - v2[axis]) + acceleration
    position = 2 * (p1[axis] - p2[axis])

    if acceleration == 0:
        if velocity == 0:
            return None if position == 0 else set()
        return {-position // velocity} if -position % velocity == 0 else set()

    discriminant = velocity * velocity - 4 * acceleration * position
    if discriminant < 0:
        return set()

    root = isqrt(discriminant)
    if root * root != discriminant:
        return set()

    times = set()
    divisor = 2 * acceleration

    for numerator in (-velocity - root, -velocity + root):
        if numerator % divisor == 0:
            times.add(numerator // divisor)

    return times


def collision_times(left, right):
    times = None

    for axis in range(3):
        axis_times = matching_times_for_axis(left, right, axis)

        if axis_times is not None and not axis_times:
            return set()
        if axis_times is None:
            continue

        if times is None:
            times = axis_times
        else:
            times &= axis_times

    if times is None:
        return {1}

    return {tick for tick in times if tick > 0}


def part1(part_data):
    particles = parse_particles(part_data)
    return min(
        range(len(particles)),
        key=lambda index: (
            manhattan(particles[index][2]),
            manhattan(particles[index][1]),
            manhattan(particles[index][0]),
        ),
    )


def part2(part_data):
    particles = parse_particles(part_data)
    collision_ticks = set()

    for left in range(len(particles)):
        for right in range(left + 1, len(particles)):
            collision_ticks.update(collision_times(particles[left], particles[right]))

    active = set(range(len(particles)))

    for tick in sorted(collision_ticks):
        positions = defaultdict(list)

        for index in active:
            positions[position_at(particles[index], tick)].append(index)

        collided = {
            index
            for indexes in positions.values()
            if len(indexes) > 1
            for index in indexes
        }
        active -= collided

    return len(active)


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
