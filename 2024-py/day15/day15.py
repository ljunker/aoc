import os

from kryptikkaocutils.Input import write_input_to_file


def try_move_2(grid, current, d):
    next = (current[0] + d[0], current[1] + d[1])
    if grid[next] == '#':
        return False
    if grid[current] == '@' and grid[next] == '.':
        return True
    if d[0] == 0:
        if grid[next] == '.':
            if grid[current] == '[':
                neighbor_next = (next[0] + 1, next[1])
                return grid[neighbor_next] == '.'
            if grid[current] == ']':
                neighbor_next = (next[0] - 1, next[1])
                return grid[neighbor_next] == '.'
        else:
            if grid[current] == '[':
                return try_move_2(grid, next, d) and try_move_2(grid, (next[0] + 1, next[1]), d)
            elif grid[current] == ']':
                return try_move_2(grid, next, d) and try_move_2(grid, (next[0] - 1, next[1]), d)
            else:
                return try_move_2(grid, next, d)
    else:
        if grid[next] == '.':
            return True
        else:
            return try_move_2(grid, next, d)

def move(grid, current, d):
    next = (current[0] + d[0], current[1] + d[1])
    if grid[current] == '@' and grid[next] == '.':
        grid[next] = grid[current]
        grid[current] = '.'
        return
    if d[0] != 0:
        if grid[next] == '.':
            grid[next] = grid[current]
        else:
            move(grid, next, d)
            grid[next] = grid[current]
        grid[current] = '.'
    else:
        if grid[current] == '[':
            neighbor_next = (next[0] + 1, next[1])
            neighbor_current = (current[0] + 1, current[1])
            if grid[next] == '.':
                grid[next] = grid[current]
            else:
                move(grid, next, d)
                grid[next] = grid[current]
            grid[current] = '.'
            if grid[neighbor_next] == '.':
                grid[neighbor_next] = grid[neighbor_current]
            else:
                move(grid, neighbor_next, d)
                grid[neighbor_next] = grid[neighbor_current]
            grid[neighbor_current] = '.'
        if grid[current] == ']':
            neighbor_next = (next[0] - 1, next[1])
            neighbor_current = (current[0] - 1, current[1])
            if grid[next] == '.':
                grid[next] = grid[current]
            else:
                move(grid, next, d)
                grid[next] = grid[current]
            grid[current] = '.'
            if grid[neighbor_next] == '.':
                grid[neighbor_next] = grid[neighbor_current]
            else:
                move(grid, neighbor_next, d)
                grid[neighbor_next] = grid[neighbor_current]
            grid[neighbor_current] = '.'





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


def part1(grid, w, h, robot, instructions):
    display_grid(grid, w, h)
    for i in instructions:
        if i == '^':
            d = (0, -1)
            if try_move(grid, robot, d):
                robot = (robot[0] + d[0], robot[1] + d[1])
        elif i == 'v':
            d = (0, 1)
            if try_move(grid, robot, d):
                robot = (robot[0] + d[0], robot[1] + d[1])
        elif i == '>':
            d = (1, 0)
            if try_move(grid, robot, d):
                robot = (robot[0] + d[0], robot[1] + d[1])
        elif i == '<':
            d = (-1, 0)
            if try_move(grid, robot, d):
                robot = (robot[0] + d[0], robot[1] + d[1])
        # display_grid(grid, w, h)
    display_grid(grid, w, h)
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


def part2(grid, w, h, robot, instructions):
    display_grid(grid, w, h)
    for i in instructions:
        if i == '^':
            d = (0, -1)
            if try_move_2(grid, robot, d):
                move(grid, robot, d)
                robot = (robot[0] + d[0], robot[1] + d[1])
        elif i == 'v':
            d = (0, 1)
            if try_move_2(grid, robot, d):
                move(grid, robot, d)
                robot = (robot[0] + d[0], robot[1] + d[1])
        elif i == '>':
            d = (1, 0)
            if try_move_2(grid, robot, d):
                move(grid, robot, d)
                robot = (robot[0] + d[0], robot[1] + d[1])
        elif i == '<':
            d = (-1, 0)
            if try_move_2(grid, robot, d):
                move(grid, robot, d)
                robot = (robot[0] + d[0], robot[1] + d[1])
        display_grid(grid, w, h)
    display_grid(grid, w, h)
    print(calc_gps(grid, w, h))


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
    if not os.path.isfile(fname):
        write_input_to_file(2024, 15, fname)
    parts = open(fname).read().split("\n\n")
    grid, w, h, robot = make_grid([line for line in parts[0].split("\n")])
    instructions = parts[1]
    part1(grid, w, h, robot, instructions)
    grid, w, h, robot = make_grid_2([line for line in parts[0].split("\n")])
    part2(grid, w, h, robot, instructions)
