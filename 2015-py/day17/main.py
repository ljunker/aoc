def read_containers(filename="i.txt"):
    containers = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line:
                containers.append(int(line))
    return containers


def find_combinations(containers, target):
    """
    Return a list of (count_used, combination)
    where combination is just True/False used containers,
    but we only care about count_used for Part 2.
    """
    n = len(containers)
    results = []

    def backtrack(i, remaining, used_count):
        if remaining == 0:
            results.append(used_count)
            return
        if i == n or remaining < 0:
            return

        # skip container i
        backtrack(i + 1, remaining, used_count)

        # use container i
        backtrack(i + 1, remaining - containers[i], used_count + 1)

    backtrack(0, target, 0)
    return results


if __name__ == "__main__":
    TARGET = 150
    containers = read_containers("i.txt")

    used_counts = find_combinations(containers, TARGET)

    # Part 1: total number of combinations
    print("Part 1 - total combinations:", len(used_counts))

    # Part 2: minimum container count + number of combinations using that many
    min_used = min(used_counts)
    ways_min = sum(1 for x in used_counts if x == min_used)

    print("Part 2 - minimum containers:", min_used)
    print("Part 2 - ways with minimum containers:", ways_min)
