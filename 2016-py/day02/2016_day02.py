from aocfw import AdventOfCodeClient, SubmissionStatus

"""
takes in a coord (x,y) and returns a number on a keypad.
keypad has the form

123
456
789
so, (0,0) is 1
(0,2) is 7
and so on
"""


def coords_to_numpad(coords):
    x, y = coords
    return y * 3 + x + 1


def part1(part_data):
    code = ""
    pos = [0, 0]
    lines = part_data.split("\n")
    for line in lines:
        for char in line:
            if char == "U":
                pos[1] -= 1
            if char == "D":
                pos[1] += 1
            if char == "L":
                pos[0] -= 1
            if char == "R":
                pos[0] += 1
            pos = [min(max(pos[0], 0), 2), min(max(pos[1], 0), 2)]
        code += str(coords_to_numpad(pos))
    return code


def part2(part_data):
    # adjacency map: from current key + direction -> new key
    moves = {
        "1": {"D": "3"},
        "2": {"R": "3", "D": "6"},
        "3": {"U": "1", "L": "2", "R": "4", "D": "7"},
        "4": {"L": "3", "D": "8"},
        "5": {"R": "6"},
        "6": {"U": "2", "L": "5", "R": "7", "D": "A"},
        "7": {"U": "3", "L": "6", "R": "8", "D": "B"},
        "8": {"U": "4", "L": "7", "R": "9", "D": "C"},
        "9": {"L": "8"},
        "A": {"U": "6", "R": "B"},
        "B": {"U": "7", "L": "A", "R": "C", "D": "D"},
        "C": {"U": "8", "L": "B"},
        "D": {"U": "B"},
    }

    code = ""
    pos = "5"  # starting position

    # strip to avoid an extra empty line at the end
    lines = part_data.strip().split("\n")

    for line in lines:
        for char in line:
            if char in moves[pos]:
                pos = moves[pos][char]
            # if move is invalid, ignore and stay on current key
        code += pos

    return code


client = AdventOfCodeClient()

data = client.get_input(2016, 2)

if __name__ == "__main__":
    answer = part1(data)
    print("Part 1:", answer)
    # res = client.submit_answer(2016, 2, 1, answer)
    # print(res.message)

    answer = part2(data)
    print("Part 2:", answer)
    res = client.submit_answer(2016, 2, 2, answer)
    print(res.message)
