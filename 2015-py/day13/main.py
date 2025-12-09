import itertools


def parse_input(filename="i.txt"):
    happiness = {}
    people = set()

    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Example:
            # "Alice would gain 54 happiness units by sitting next to Bob."
            parts = line.split()
            a = parts[0]
            sign = 1 if parts[2] == "gain" else -1
            units = int(parts[3]) * sign
            b = parts[-1].rstrip(".")

            people.add(a)
            people.add(b)
            happiness[(a, b)] = units

    return people, happiness


def total_happiness(order, happiness):
    """Compute total happiness for a circular seating order."""
    total = 0
    n = len(order)
    for i in range(n):
        a = order[i]
        b = order[(i + 1) % n]  # neighbor to the right (wrap)
        total += happiness.get((a, b), 0)
        total += happiness.get((b, a), 0)
    return total


def find_best_happiness(people, happiness):
    # Fix one person to break rotational symmetry
    people = list(people)
    first = people[0]
    others = people[1:]

    best = None
    best_order = None

    for perm in itertools.permutations(others):
        order = (first,) + perm
        score = total_happiness(order, happiness)
        if best is None or score > best:
            best = score
            best_order = order

    return best, best_order


def add_yourself(people, happiness, name="you"):
    """Add yourself with 0 happiness with everyone (both directions)."""
    for p in people:
        happiness[(name, p)] = 0
        happiness[(p, name)] = 0
    people = set(people)
    people.add(name)
    return people, happiness


if __name__ == "__main__":
    people, happiness = parse_input("i.txt")

    # Part 1
    best1, order1 = find_best_happiness(people, happiness)
    print("Part 1 - best total happiness:", best1)

    # Part 2: add yourself
    people2, happiness2 = add_yourself(people, dict(happiness))  # copy dict
    best2, order2 = find_best_happiness(people2, happiness2)
    print("Part 2 - best total happiness (with you):", best2)
