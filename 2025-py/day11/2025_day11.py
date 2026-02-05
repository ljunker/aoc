import hashlib
from collections import Counter
from functools import lru_cache

from aocfw import AdventOfCodeClient

YEAR = 2025
DAY = 11

def parse_input(lines):
    graph = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        left, right = line.split(":", 1)
        src = left.strip()
        targets = right.strip().split()
        graph[src] = targets
    return graph

def count_paths(graph, start="you", target="out"):
    @lru_cache(maxsize=None)
    def dfs(node):
        if node == target:
            return 1
        total = 0
        for nxt in graph.get(node, []):
            total += dfs(nxt)
        return total

    return dfs(start)


def count_paths_with_dac_fft(graph, start="svr", target="out", dac="dac", fft="fft"):
    @lru_cache(maxsize=None)
    def dfs(node, seen_dac, seen_fft):
        # Update flags when we arrive at this node
        if node == dac:
            seen_dac = True
        if node == fft:
            seen_fft = True

        # If we reached the output, only count this path if both were seen
        if node == target:
            return 1 if (seen_dac and seen_fft) else 0

        total = 0
        for nxt in graph.get(node, []):
            total += dfs(nxt, seen_dac, seen_fft)
        return total

    return dfs(start, False, False)

def part1(part_data):
    lines = part_data.split("\n")
    graph = parse_input(lines)
    result = count_paths(graph, start="you", target="out")
    return result

def part2(part_data):
    lines = part_data.split("\n")
    graph = parse_input(lines)
    result = count_paths_with_dac_fft(graph, start="svr", target="out",
                                      dac="dac", fft="fft")
    return result


if __name__ == "__main__":
    client = AdventOfCodeClient()

    data = client.get_input(YEAR, DAY)
    answer = part1(data)
    print("Part 1:", answer)
    # res = client.submit_answer(YEAR, DAY, 1, answer)
    # print(res.message)

    answer = part2(data)
    print("Part 2:", answer)
    # res = client.submit_answer(YEAR, DAY, 2, answer)
    # print(res.message)
