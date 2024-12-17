from heapq import heapify, heappop, heappush

from kryptikkaocutils.Timer import timer


class Object:
    def __init__(self, name):
        self.name = name
        self.moons = []
        self.orbits = None

    def add_moon(self, moon):
        self.moons.append(moon)
        moon.orbits = self

    def count_moons(self):
        count = len(self.moons)

        return len(self.moons) + sum([moon.count_moons() for moon in self.moons])


@timer
def part1(lines):
    objects = make_system(lines)
    print(sum([objects[o].count_moons() for o in objects]))

@timer
def part2(lines):
    objects = make_system(lines)
    start = objects["YOU"].orbits
    end = objects["SAN"].orbits
    dist = {objects[o]: 1e7 for o in objects}
    dist[start] = 0
    pq = [(0, start)]
    visited = set()

    while pq:
        pq = sorted(pq, key=lambda x: x[0])
        (current_dist, current) = pq.pop(0)
        if current == end:
            break
        if current in visited:
            continue
        visited.add(current)

        neighbors = current.moons
        if current.orbits is not None:
            neighbors += [current.orbits]

        for neighbor in neighbors:
            tentative_dist = current_dist + 1
            if tentative_dist < dist[neighbor]:
                dist[neighbor] = tentative_dist
                pq.append((tentative_dist, neighbor))
    print(dist[end])

def make_system(lines):
    COM = Object("COM")
    objects = {"COM": COM}
    for l in lines:
        c_name, m_name = l.strip().split(")")
        c = get_object(c_name, objects)
        m = get_object(m_name, objects)
        c.add_moon(m)
    return objects


def get_object(name, objects):
    if name in objects:
        c = objects[name]
    else:
        c = Object(name)
        objects[name] = c
    return c


if __name__ == "__main__":
    part1(open("i.txt").readlines())
    part2(open("i.txt").readlines())