from kryptikkaocutils.Timer import timer

grid_size = 71

f = open("i.txt")
b = []
for l in f.readlines():
    x, y = [int(num) for num in l.split(",")]
    b.append((x, y))


def search_for_end(cutoff):
    grid = {}
    for y in range(grid_size):
        for x in range(grid_size):
            grid[(x, y)] = 0
    for i in range(cutoff):
        grid[b[i]] = 1
    start = (0, 0)
    end = (grid_size - 1, grid_size - 1)
    dist = {p: 1e10 for p in grid}
    dist[start] = 0
    pq = [(0, start)]
    visited = set()
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def add(t1, t2):
        return tuple(map(sum, zip(t1, t2)))

    def is_in_bounds(n):
        return 0 <= n[0] < grid_size and 0 <= n[1] < grid_size

    while pq:
        pq = sorted(pq, key=lambda x: x[0])
        (current_dist, current) = pq.pop(0)
        if current == end:
            break
        if current in visited:
            continue
        visited.add(current)

        neighbors = []
        for d in dirs:
            neighbor = add(current, d)
            if is_in_bounds(neighbor) and grid[neighbor] != 1:
                neighbors.append(add(current, d))
        for neighbor in neighbors:
            tentative_d = current_dist + 1
            if tentative_d < dist[neighbor]:
                dist[neighbor] = tentative_d
                pq.append((tentative_d, neighbor))
    return dist[end] if end in dist else None

@timer
def part1():
    print("p1:", search_for_end(1024))

@timer
def part2():
    left, right = 1024, len(b)
    while True:
        mid = (left + right) // 2
        if left + 1 == right:
            break
        if search_for_end(mid) == 1e10:
            right = mid
        else:
            left = mid
    print("p2:", b[left])

part1()
part2()