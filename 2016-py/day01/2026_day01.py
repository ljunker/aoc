from aocfw import AdventOfCodeClient, SubmissionStatus


def part1(part_data):
    pos, facing = [0, 0], 0
    for direction in part_data.split(','):
        direction = direction.strip()
        direction, amount = direction[0], int(direction[1:])
        if direction == 'L':
            facing = (facing + 3) % 4
        if direction == 'R':
            facing = (facing + 1) % 4
        if facing == 0:
            pos = (pos[0], pos[1] - amount)
        if facing == 1:
            pos = (pos[0] + amount, pos[1])
        if facing == 2:
            pos = (pos[0], pos[1] + amount)
        if facing == 3:
            pos = (pos[0] - amount, pos[1])
    return abs(pos[0]) + abs(pos[1])

def part2(part_data):
    pos, facing = [0, 0], 0
    visited = set()
    for direction in part_data.split(','):
        direction = direction.strip()
        direction, amount = direction[0], int(direction[1:])
        if direction == 'L':
            facing = (facing + 3) % 4
        if direction == 'R':
            facing = (facing + 1) % 4
        for _ in range(amount):
            if facing == 0:
                pos = (pos[0], pos[1] - 1)
            if facing == 1:
                pos = (pos[0] + 1, pos[1])
            if facing == 2:
                pos = (pos[0], pos[1] + 1)
            if facing == 3:
                pos = (pos[0] - 1, pos[1])
            if pos in visited:
                return abs(pos[0]) + abs(pos[1])
            visited.add(pos)


client = AdventOfCodeClient()

data = client.get_input(2016, 1)

if __name__ == "__main__":
    answer = part1(data)
    print("Part 1:", answer)

    answer = part2(data)
    print("Part 2:", answer)
