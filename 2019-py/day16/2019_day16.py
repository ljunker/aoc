import time
from itertools import accumulate

from aocfw import AdventOfCodeClient

YEAR = 2019
DAY = 16


def fft_phase(signal):
    prefix = list(accumulate(signal, initial=0))
    length = len(signal)
    output = []
    for width in range(1, length + 1):
        total = 0
        # After skipping the first pattern element, the first +1 block
        # starts at width - 1. The -1 block follows two blocks later.
        for start in range(width - 1, length, 4 * width):
            total += prefix[min(start + width, length)] - prefix[start]
            negative_start = start + 2 * width
            if negative_start < length:
                total -= prefix[min(negative_start + width, length)] - prefix[negative_start]
        output.append(abs(total) % 10)
    return output


def part1(part_data):
    signal = list(map(int, part_data.strip()))
    for _ in range(100):
        signal = fft_phase(signal)
    return "".join(map(str, signal[:8]))


def part2(part_data):
    data = part_data.strip()
    offset = int(data[:7])
    length = len(data) * 10_000
    if not length // 2 <= offset <= length - 8:
        raise ValueError("Expected an eight-digit message in the second half of the signal")

    digits = bytearray(map(int, data))
    first_copy, start = divmod(offset, len(digits))
    suffix = digits[start:] + digits * (9_999 - first_copy)
    # In this half, each pattern has only +1 coefficients from its
    # output position through the end of the signal.
    for _ in range(100):
        total = 0
        for index in range(len(suffix) - 1, -1, -1):
            total = (total + suffix[index]) % 10
            suffix[index] = total
    return "".join(map(str, suffix[:8]))


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
