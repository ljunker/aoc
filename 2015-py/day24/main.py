import itertools
import math


def read_weights(filename="i.txt"):
    weights = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line:
                weights.append(int(line))
    return weights


def multiset_remove(pool, subset):
    """Remove the elements of subset from pool (multiset removal)."""
    pool = list(pool)
    for x in subset:
        pool.remove(x)  # removes one occurrence
    return pool


def can_partition_k_groups(nums, k, target):
    """
    Check if nums can be partitioned into k groups of sum == target.
    Standard k-partition backtracking.
    """
    if sum(nums) != k * target:
        return False

    nums = sorted(nums, reverse=True)
    buckets = [0] * k

    def backtrack(index):
        if index == len(nums):
            # All numbers used; by construction, each bucket <= target
            return all(b == target for b in buckets)

        v = nums[index]
        for i in range(k):
            if buckets[i] + v <= target:
                buckets[i] += v
                if backtrack(index + 1):
                    return True
                buckets[i] -= v
            # Symmetry break: if this bucket was empty and didn't work,
            # no point trying other empty buckets.
            if buckets[i] == 0:
                break
        return False

    return backtrack(0)


def find_best_qe(weights, groups):
    """
    Find the minimal quantum entanglement for group 1 when splitting
    into `groups` equal-weight groups, with minimal number of packages
    in group 1 and minimal QE among those.
    """
    total = sum(weights)
    assert total % groups == 0, "Total weight must be divisible by number of groups"
    target = total // groups

    weights = sorted(weights, reverse=True)

    best_qe = None

    # We search by increasing size of group 1
    for size in range(1, len(weights) + 1):
        valid_first_groups = []

        # All combos of given size that sum to target
        for combo in itertools.combinations(weights, size):
            if sum(combo) == target:
                valid_first_groups.append(combo)

        if not valid_first_groups:
            continue

        # For this minimal size, we only keep those where the remaining
        # can be partitioned into (groups - 1) equal groups.
        for combo in valid_first_groups:
            remaining = multiset_remove(weights, combo)

            if can_partition_k_groups(remaining, groups - 1, target):
                qe = math.prod(combo)
                if best_qe is None or qe < best_qe:
                    best_qe = qe

        # If we found any solution for this size, that's the minimal size;
        # we don't look at larger sizes.
        if best_qe is not None:
            break

    return best_qe


if __name__ == "__main__":
    weights = read_weights("i.txt")

    # Part 1: 3 groups
    part1_qe = find_best_qe(weights, groups=3)
    print("Part 1 - minimal quantum entanglement (3 groups):", part1_qe)

    # Part 2: 4 groups
    part2_qe = find_best_qe(weights, groups=4)
    print("Part 2 - minimal quantum entanglement (4 groups):", part2_qe)
