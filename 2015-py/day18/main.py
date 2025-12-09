def read_grid(filename="i.txt"):
    grid = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            grid.append([c == "#" for c in line])
    return grid


def count_on(grid):
    return sum(cell for row in grid for cell in row)


def step(grid):
    """Normal Game of Life step (Part 1 rules)."""
    h = len(grid)
    w = len(grid[0])
    new = [[False] * w for _ in range(h)]

    for y in range(h):
        for x in range(w):
            on_neighbors = 0
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dy == 0 and dx == 0:
                        continue
                    ny = y + dy
                    nx = x + dx
                    if 0 <= ny < h and 0 <= nx < w:
                        if grid[ny][nx]:
                            on_neighbors += 1

            if grid[y][x]:
                new[y][x] = on_neighbors in (2, 3)
            else:
                new[y][x] = (on_neighbors == 3)

    return new


def force_corners_on(grid):
    """Force the four corners to be on."""
    h = len(grid)
    w = len(grid[0])
    grid[0][0] = True
    grid[0][w - 1] = True
    grid[h - 1][0] = True
    grid[h - 1][w - 1] = True


if __name__ == "__main__":
    # Part 1
    grid1 = read_grid("i.txt")
    for _ in range(100):
        grid1 = step(grid1)
    print("Part 1 - lights on after 100 steps:", count_on(grid1))

    # Part 2: corners stuck on
    grid2 = read_grid("i.txt")
    force_corners_on(grid2)  # corners are stuck on from the start
    for _ in range(100):
        grid2 = step(grid2)
        force_corners_on(grid2)
    print("Part 2 - lights on after 100 steps with stuck corners:", count_on(grid2))
