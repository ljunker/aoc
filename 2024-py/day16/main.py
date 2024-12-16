import queue

from kryptikkaocutils.Timer import timer


def make_grid(lines):
    start = (-1, -1)
    end = (-1, -1)
    grid = {}
    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if c == 'S':
                start = (x, y)
            if c == 'E':
                end = (x, y)
            grid[(x, y)] = c
    return grid, len(lines[0]), len(lines), start, end


@timer
def part1(grid, w, h, start, end):
    dirs = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    routes = []
    visited = {}

    queue = [(start, [start], 0, 0)]
    while queue:
        (x,y), history, score, d = queue.pop(0)
        if (x, y) == end:
            routes.append((history, score))
            continue
        if ((x, y), d) in visited and visited[((x, y), d)] < score:
            continue
        visited[((x, y), d)] = score
        for _d, (dx, dy) in enumerate(dirs):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and grid[(nx, ny)] != '#' and (nx, ny) not in history:
                if _d == d:
                    queue.append(((nx, ny), history + [(nx, ny)], score + 1, _d))
                else:
                    queue.append(((x, y), history + [], score + 1000, _d))

    return routes


@timer
def part2():
    best = [r for r in routes if r[1] == min_score]
    tiles = {tile for route in best for tile in route[0]}
    return len(tiles)


if __name__ == "__main__":
    fname = "i.txt"
    grid, w, h, start, end = make_grid([line for line in open(fname).read().split("\n")])
    routes = part1(grid, w, h, start, end)

    min_score = min(r[1] for r in routes)
    print(min_score)
    # part 2
    print(part2())
