from IntComputer.computer import IntComputer

def add(t1, t2):
    return tuple(map(sum, zip(t1, t2)))

if __name__ == "__main__":
    program = [int(num) for num in open("program.txt").read().split(",")]

    dirs = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    grid = {}
    c = IntComputer(program, True, True)
    current = (0, 0)
    grid[current] = 1
    painted = set()
    current_dir = 0
    def get_current_color(pos):
        if pos in grid:
            return grid[pos]
        else:
            grid[current] = 0
            return 0
    finished = False
    c.piped_input.append(get_current_color(current))
    while True:
        finished = c.run_program()
        if finished:
            break
        while len(c.piped_output) > 0:
            paint = c.piped_output.pop(0)
            grid[current] = paint
            painted.add(current)
            turn = c.piped_output.pop(0)
            current_dir += 1 if turn == 0 else -1
            current_dir %= 4
            current = add(current, dirs[current_dir])
        c.piped_input.append(get_current_color(current))
    print(len(painted))
    for y in range(6):
        for x in range(100):
            if (x,y) in grid:
                print('█' if grid[(x,y)] == 1 else ' ', end='')
            else:
                print('█', end='')
        print()