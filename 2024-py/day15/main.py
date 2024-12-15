from kryptikkaocutils.Timer import timer

def try_move_2(grid, current, d):
    next = (current[0] + d[0], current[1] + d[1])
    if grid[next] == '#':
        return False
    if grid[next] == '.':
        return True
    if d[0] == 0:
        if grid[next] == '[':
            neighbor = (next[0] + 1, next[1])
            return try_move_2(grid, next, d) and try_move_2(grid, neighbor, d)
        elif grid[next] == ']':
            neighbor = (next[0] - 1, next[1])
            return try_move_2(grid, next, d) and try_move_2(grid, neighbor, d)
        else:
            return try_move_2(grid, next, d)
    else:
        return try_move_2(grid, next, d)


def move(grid, current, d):
    next = (current[0] + d[0], current[1] + d[1])
    if d[0] != 0:
        if grid[next] != '.':
            move(grid, next, d)
    else:
        if grid[next] != '.':
            if grid[next] == '[':
                neighbor = (next[0] + 1, next[1])
                move(grid, next, d)
                move(grid, neighbor, d)
            elif grid[next] == ']':
                neighbor = (next[0] - 1, next[1])
                move(grid, next, d)
                move(grid, neighbor, d)
    grid[next] = grid[current]
    grid[current] = '.'


def try_move(grid, current, d):
    next = (current[0] + d[0], current[1] + d[1])
    if grid[next] == '#':
        return False
    if grid[next] == 'O':
        if try_move(grid, next, d):
            grid[next] = grid[current]
            grid[current] = '.'
            return True
    if grid[next] == '.':
        grid[next] = grid[current]
        grid[current] = '.'
        return True


def arrow_to_dir(a):
    if a == '^':
        return (0, -1)
    elif a == 'v':
        return (0, 1)
    elif a == '>':
        return (1, 0)
    elif a == '<':
        return (-1, 0)


@timer
def part1(grid, w, h, robot, instructions):
    #display_grid(grid, w, h)
    for i in instructions:
        if i == '\n':
            continue
        d = arrow_to_dir(i)
        if try_move(grid, robot, d):
            robot = (robot[0] + d[0], robot[1] + d[1])
        # display_grid(grid, w, h)
    #display_grid(grid, w, h)
    print(calc_gps(grid, w, h))


def display_grid(grid, w, h):
    for y in range(h):
        for x in range(w):
            print(grid[(x, y)], end='')
        print()
    print("==========================")


def calc_gps(grid, w, h):
    s = 0
    for y in range(h):
        for x in range(w):
            if grid[(x, y)] == 'O':
                s += 100 * y + x
    return s


def calc_gps_2(grid, w, h):
    s = 0
    for y in range(h):
        for x in range(w):
            if grid[(x, y)] == '[':
                s += 100 * y + x
    return s


@timer
def part2(grid, w, h, robot, instructions):
    #display_grid(grid, w, h)
    for i in instructions:
        if i == '\n':
            continue
        d = arrow_to_dir(i)
        if try_move_2(grid, robot, d):
            move(grid, robot, d)
            robot = (robot[0] + d[0], robot[1] + d[1])
        #display_grid(grid, w, h)
    #display_grid(grid, w, h)
    print(calc_gps_2(grid, w, h))


def make_grid_2(lines):
    newLines = []
    for l in lines:
        nl = ""
        for c in l:
            if c == '#':
                nl += '##'
            if c == '@':
                nl += '@.'
            if c == 'O':
                nl += '[]'
            if c == '.':
                nl += '..'
        newLines.append(nl)
    grid = {}
    robot = (-1, -1)
    for y, line in enumerate(newLines):
        for x, c in enumerate(line):
            grid[(x, y)] = c
            if c == "@":
                robot = (x, y)
    return grid, len(newLines[0]), len(newLines), robot


def make_grid(lines):
    grid = {}
    robot = (-1, -1)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            grid[(x, y)] = c
            if c == "@":
                robot = (x, y)
    return grid, len(lines[0]), len(lines), robot


if __name__ == "__main__":
    fname = "i.txt"
    parts = open(fname).read().split("\n\n")
    grid, w, h, robot = make_grid([line for line in parts[0].split("\n")])
    instructions = parts[1]
    part1(grid, w, h, robot, instructions)
    grid, w, h, robot = make_grid_2([line for line in parts[0].split("\n")])
    part2(grid, w, h, robot, instructions)
