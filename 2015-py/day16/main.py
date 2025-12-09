import re

# MFCSAM readings
MFCSAM = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


def parse_input(filename="i.txt"):
    """
    Parse lines like:
    Sue 1: cars: 9, akitas: 3, goldfish: 0
    """
    sues = {}
    pattern = re.compile(r"^Sue (\d+): (.*)$")

    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            m = pattern.match(line)
            if not m:
                raise ValueError(f"Cannot parse line: {line}")
            sue_num = int(m.group(1))
            rest = m.group(2)

            props = {}
            for part in rest.split(", "):
                name, value = part.split(": ")
                props[name] = int(value)

            sues[sue_num] = props

    return sues


def matches_part1(sue_props, mfcsam):
    """
    Part 1 rules:
    Every property listed for this Sue must match MFCSAM exactly.
    """
    for k, v in sue_props.items():
        if k in mfcsam and mfcsam[k] != v:
            return False
    return True


def matches_part2(sue_props, mfcsam):
    """
    Part 2 rules:
      - cats, trees: Sue's value > MFCSAM value
      - pomeranians, goldfish: Sue's value < MFCSAM value
      - everything else: equality
    """
    for k, v in sue_props.items():
        if k not in mfcsam:
            continue

        ref = mfcsam[k]
        if k in ("cats", "trees"):
            if not (v > ref):
                return False
        elif k in ("pomeranians", "goldfish"):
            if not (v < ref):
                return False
        else:
            if v != ref:
                return False

    return True


if __name__ == "__main__":
    sues = parse_input("i.txt")

    # Part 1
    part1_candidates = [num for num, props in sues.items() if matches_part1(props, MFCSAM)]
    print("Part 1 matching Sues:", part1_candidates)

    # Part 2
    part2_candidates = [num for num, props in sues.items() if matches_part2(props, MFCSAM)]
    print("Part 2 matching Sues:", part2_candidates)
