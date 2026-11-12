import time

from aocfw import AdventOfCodeClient
from IntComputer.computer import IntComputer

YEAR = 2019
DAY = 17

DIRECTIONS = {"^": -1j, ">": 1, "v": 1j, "<": -1}
FUNCTION_NAMES = "ABC"
ROUTINE_LIMIT = 20


def camera_view(data):
    computer = IntComputer(
        map(int, data.strip().split(",")),
        input_piped_mode=True,
        output_piped_mode=True,
    )
    if not computer.run_program():
        raise ValueError("Camera program requested input")
    return "".join(map(chr, computer.piped_output))


def scaffold_map(view):
    scaffold = set()
    robot = None
    for y, row in enumerate(view.splitlines()):
        for x, tile in enumerate(row):
            position = complex(x, y)
            if tile == "#" or tile in DIRECTIONS:
                scaffold.add(position)
            if tile in DIRECTIONS:
                robot = position, DIRECTIONS[tile]
    return scaffold, robot


def alignment_sum(scaffold):
    return sum(
        int(position.real * position.imag)
        for position in scaffold
        if all(position + step in scaffold for step in DIRECTIONS.values())
    )


def trace_route(scaffold, position, heading):
    visited = {position}
    turn_points = set()
    route = []
    while True:
        if (position, heading) in turn_points:
            raise ValueError("Scaffold route loops")
        turn_points.add((position, heading))
        for turn, direction in (("L", heading * -1j), ("R", heading * 1j)):
            if position + direction in scaffold:
                heading = direction
                break
        else:
            break

        distance = 0
        while position + heading in scaffold:
            position += heading
            visited.add(position)
            distance += 1
        route.extend((turn, str(distance)))

    if visited != scaffold:
        raise ValueError("Route did not cover all scaffold")
    return tuple(route)


def compress_route(route):
    def search(offset, main, functions):
        if offset == len(route):
            return (main, functions) if len(functions) == len(FUNCTION_NAMES) else None
        if len(",".join(main + ("A",))) > ROUTINE_LIMIT:
            return None

        for name, function in zip(FUNCTION_NAMES, functions):
            end = offset + len(function)
            if route[offset:end] == function:
                result = search(end, main + (name,), functions)
                if result is not None:
                    return result

        if len(functions) < len(FUNCTION_NAMES):
            name = FUNCTION_NAMES[len(functions)]
            for end in range(offset + 2, len(route) + 1, 2):
                function = route[offset:end]
                if len(",".join(function)) > ROUTINE_LIMIT:
                    break
                result = search(end, main + (name,), functions + (function,))
                if result is not None:
                    return result
        return None

    result = search(0, (), ())
    if result is None:
        raise ValueError("Route cannot be compressed into three functions")
    return result


def part1(part_data):
    scaffold, _ = scaffold_map(camera_view(part_data))
    return alignment_sum(scaffold)


def part2(part_data):
    scaffold, robot = scaffold_map(camera_view(part_data))
    if robot is None:
        raise ValueError("Camera view does not show the robot")
    main, functions = compress_route(trace_route(scaffold, *robot))
    commands = "\n".join(",".join(line) for line in (main, *functions, ("n",))) + "\n"

    computer = IntComputer(
        map(int, part_data.strip().split(",")),
        input_piped_mode=True,
        output_piped_mode=True,
    )
    computer.program[0] = 2
    computer.piped_input.extend(map(ord, commands))
    halted = computer.run_program()
    if not halted or not computer.piped_output or computer.piped_output[-1] <= 255:
        raise ValueError("Vacuum robot did not report a dust count")
    return computer.piped_output[-1]


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
