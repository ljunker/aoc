from bisect import bisect_left

from collections import defaultdict, deque
import sys

from kryptikkaocutils.Timer import timer

sys.setrecursionlimit(10000)

input_file = 'input.txt'
test_file = 'sample.txt'

directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
inf = float('inf')



def get_endpoints(grid):
    start = None
    end = None

    for r in range(R):
        for c in range(C):
            if grid[r][c] == 'S':
                start = (r, c)
            elif grid[r][c] == 'E':
                end = r, c

    return start, end


def get_distances(grid, end):
    distances = defaultdict(lambda: inf)
    q = deque([(end, 0)])
    visited = set()
    while q:
        pos, d = q.popleft()
        if pos in visited:
            continue
        visited.add(pos)
        r, c = pos
        distances[(r, c)] = d
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (nr, nc) not in visited and grid[nr][nc] != '#':
                q.append([(nr, nc), d + 1])

    return distances



def dist(pos1, pos2):
    r1, c1 = pos1
    r2, c2 = pos2
    return abs(r1 - r2) + abs(c1 - c2)


def num_cheating_paths(distances, saving_threshold, cheat_duration):
    total_saved = defaultdict(int)
    distance_list = [(d, pos) for pos, d in distances.items()]
    distance_list.sort()
    n = len(distance_list)
    for i in range(n):
        d1, pos1 = distance_list[i]
        j = bisect_left(distance_list, (d1 + saving_threshold - 1, (-1, -1)))
        for k in range(j, n):
            d2, pos2 = distance_list[k]
            if dist(pos1, pos2) > cheat_duration:
                continue
            saved = (d2 - d1) - dist(pos1, pos2)
            if saved >= saving_threshold:
                total_saved[saved] += 1

    return sum(total_saved.values())

@timer
def part1():
    print(num_cheating_paths(distances, 100, 2))

@timer
def part2():
    print(num_cheating_paths(distances, 100, 20))


if __name__ == "__main__":
    with open(input_file, 'r') as file:
        lines = file.readlines()
        grid = [row.strip() for row in lines]
        R, C = len(grid), len(grid[0])
    start, end = get_endpoints(grid)
    distances = get_distances(grid, end)
    part1()
    part2()
