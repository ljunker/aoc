import itertools


def parse_input(lines):
    distances = {}
    cities = set()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Example: "London to Dublin = 464"
        parts = line.split()
        a, b, d = parts[0], parts[2], int(parts[4])

        cities.add(a)
        cities.add(b)

        distances[(a, b)] = d
        distances[(b, a)] = d  # undirected

    return cities, distances


def route_distance(route, distances):
    total = 0
    for i in range(len(route) - 1):
        d = distances.get((route[i], route[i + 1]))
        if d is None:
            return None
        total += d
    return total


def solve(cities, distances):
    shortest = None
    longest = None

    for perm in itertools.permutations(cities):
        dist = route_distance(perm, distances)
        if dist is None:
            continue

        if shortest is None or dist < shortest:
            shortest = dist

        if longest is None or dist > longest:
            longest = dist

    return shortest, longest


if __name__ == '__main__':
    fname = "i.txt"
    with open(fname) as f:
        lines = f.readlines()
        cities, distances = parse_input(lines)
        shortest, longest = solve(cities, distances)
        print(shortest)
        print(longest)