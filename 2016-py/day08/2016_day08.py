import time

from aocfw import AdventOfCodeClient

YEAR = 2016
DAY = 8

WIDTH = 50
HEIGHT = 6

FONT_ROWS = {
    "A": (".##.", "#..#", "#..#", "####", "#..#", "#..#"),
    "B": ("###.", "#..#", "###.", "#..#", "#..#", "###."),
    "C": (".##.", "#..#", "#...", "#...", "#..#", ".##."),
    "E": ("####", "#...", "###.", "#...", "#...", "####"),
    "F": ("####", "#...", "###.", "#...", "#...", "#..."),
    "G": (".##.", "#..#", "#...", "#.##", "#..#", ".###"),
    "H": ("#..#", "#..#", "####", "#..#", "#..#", "#..#"),
    "I": (".###", "..#.", "..#.", "..#.", "..#.", ".###"),
    "J": ("..##", "...#", "...#", "...#", "#..#", ".##."),
    "K": ("#..#", "#.#.", "##..", "#.#.", "#.#.", "#..#"),
    "L": ("#...", "#...", "#...", "#...", "#...", "####"),
    "O": (".##.", "#..#", "#..#", "#..#", "#..#", ".##."),
    "P": ("###.", "#..#", "#..#", "###.", "#...", "#..."),
    "R": ("###.", "#..#", "#..#", "###.", "#.#.", "#..#"),
    "U": ("#..#", "#..#", "#..#", "#..#", "#..#", ".##."),
    "Y": ("#...", "#...", ".#..", "..#.", "..#.", "..#."),
    "Z": ("####", "...#", "..#.", ".#..", "#...", "####"),
}
FONT = {"".join(rows): letter for letter, rows in FONT_ROWS.items()}


def lit_char(is_lit):
    return "#" if is_lit else "."


def run_screen(part_data, width=WIDTH, height=HEIGHT):
    screen = [[False for _ in range(width)] for _ in range(height)]

    for line in part_data.splitlines():
        if line.startswith("rect "):
            dims = line.removeprefix("rect ").split("x")
            rect_width, rect_height = [int(dim) for dim in dims]
            for y in range(rect_height):
                for x in range(rect_width):
                    screen[y][x] = True
        elif line.startswith("rotate row "):
            y, amount = [int(num) for num in line.split("=")[1].split(" by ")]
            amount %= width
            screen[y] = screen[y][-amount:] + screen[y][:-amount]
        elif line.startswith("rotate column "):
            x, amount = [int(num) for num in line.split("=")[1].split(" by ")]
            amount %= height
            column = [screen[y][x] for y in range(height)]
            column = column[-amount:] + column[:-amount]
            for y, value in enumerate(column):
                screen[y][x] = value
        else:
            raise ValueError(f"Unknown instruction: {line}")

    return screen


def render(screen):
    return "\n".join("".join(lit_char(cell) for cell in row) for row in screen)


def decode(screen):
    letters = []
    for offset in range(0, len(screen[0]), 5):
        block = "".join(
            lit_char(screen[y][x])
            for y in range(len(screen))
            for x in range(offset, min(offset + 4, len(screen[0])))
        )
        letters.append(FONT.get(block, "?"))
    return "".join(letters)


def part1(part_data):
    return sum(cell for row in run_screen(part_data) for cell in row)


def part2(part_data):
    screen = run_screen(part_data)
    answer = decode(screen)
    if "?" not in answer:
        return answer
    return "\n" + render(screen)


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
