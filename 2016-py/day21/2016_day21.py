import time

from aocfw import AdventOfCodeClient

YEAR = 2016
DAY = 21
START_TEXT = "abcdefgh"
SCRAMBLED_TEXT = "fbgdceah"


def rotate(text, steps):
    steps %= len(text)
    return text[-steps:] + text[:-steps] if steps else text


def move(text, source, target):
    letters = list(text)
    letter = letters.pop(source)
    letters.insert(target, letter)
    return "".join(letters)


def apply_instruction(text, instruction):
    parts = instruction.split()

    if parts[0] == "swap" and parts[1] == "position":
        first = int(parts[2])
        second = int(parts[5])
        letters = list(text)
        letters[first], letters[second] = letters[second], letters[first]
        return "".join(letters)

    if parts[0] == "swap" and parts[1] == "letter":
        first = parts[2]
        second = parts[5]
        return text.translate(str.maketrans({first: second, second: first}))

    if parts[0] == "rotate" and parts[1] in {"left", "right"}:
        steps = int(parts[2])
        return rotate(text, steps if parts[1] == "right" else -steps)

    if parts[0] == "rotate" and parts[1] == "based":
        index = text.index(parts[-1])
        steps = 1 + index + (1 if index >= 4 else 0)
        return rotate(text, steps)

    if parts[0] == "reverse":
        start = int(parts[2])
        end = int(parts[4])
        return text[:start] + text[start:end + 1][::-1] + text[end + 1:]

    if parts[0] == "move":
        return move(text, int(parts[2]), int(parts[5]))

    raise ValueError(f"Unknown instruction: {instruction}")


def reverse_instruction(text, instruction):
    parts = instruction.split()

    if parts[0] in {"swap", "reverse"}:
        return apply_instruction(text, instruction)

    if parts[0] == "rotate" and parts[1] in {"left", "right"}:
        direction = "left" if parts[1] == "right" else "right"
        return apply_instruction(text, f"rotate {direction} {parts[2]} steps")

    if parts[0] == "rotate" and parts[1] == "based":
        for steps in range(len(text)):
            candidate = rotate(text, -steps)
            if apply_instruction(candidate, instruction) == text:
                return candidate

        raise ValueError(f"Cannot reverse instruction: {instruction}")

    if parts[0] == "move":
        return move(text, int(parts[5]), int(parts[2]))

    raise ValueError(f"Unknown instruction: {instruction}")


def scramble(part_data, text):
    result = text
    for instruction in part_data.splitlines():
        if instruction.strip():
            result = apply_instruction(result, instruction)

    return result


def unscramble(part_data, text):
    result = text
    instructions = [line for line in part_data.splitlines() if line.strip()]
    for instruction in reversed(instructions):
        result = reverse_instruction(result, instruction)

    return result


def part1(part_data):
    return scramble(part_data, START_TEXT)


def part2(part_data):
    return unscramble(part_data, SCRAMBLED_TEXT)


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
