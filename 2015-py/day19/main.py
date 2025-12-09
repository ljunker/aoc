def parse_input(filename="i.txt"):
    """
    Parse replacement rules and the medicine molecule from i.txt.

    Expected format, e.g.:

        H => HO
        H => OH
        O => HH

        HOH
    """
    rules = []
    molecule = None

    with open(filename) as f:
        lines = [line.rstrip("\n") for line in f]

    i = 0
    # Read rules until blank line
    while i < len(lines) and lines[i].strip():
        line = lines[i].strip()
        left, _, right = line.partition(" => ")
        rules.append((left, right))
        i += 1

    # Skip blank lines
    while i < len(lines) and not lines[i].strip():
        i += 1

    # Next non-empty line is the medicine molecule
    if i < len(lines):
        molecule = lines[i].strip()

    return rules, molecule


def distinct_molecules_after_one_step(rules, molecule):
    """
    Generate all distinct molecules after exactly one replacement.
    """
    results = set()

    for src, dst in rules:
        start = 0
        L = len(src)
        # Find all occurrences of src in molecule (including overlapping)
        while True:
            idx = molecule.find(src, start)
            if idx == -1:
                break
            new_mol = molecule[:idx] + dst + molecule[idx + L:]
            results.add(new_mol)
            start = idx + 1  # keep looking for further occurrences

    return results


def tokenize_molecule(molecule):
    """
    Split molecule into element tokens: capital letter + optional lowercase.
    Example: "CRnCaSiRn..." -> ['C', 'Rn', 'Ca', 'Si', 'Rn', ...]
    """
    tokens = []
    i = 0
    while i < len(molecule):
        ch = molecule[i]
        if ch.isupper():
            # Start of a new element
            if i + 1 < len(molecule) and molecule[i + 1].islower():
                tokens.append(molecule[i:i+2])
                i += 2
            else:
                tokens.append(ch)
                i += 1
    return tokens


def steps_from_e_formula(molecule):
    """
    AoC-specific grammar trick for Part 2:

    Minimal steps = (#tokens) - (#Rn) - (#Ar) - 2*(#Y) - 1
    """
    tokens = tokenize_molecule(molecule)
    n = len(tokens)
    rn = tokens.count("Rn")
    ar = tokens.count("Ar")
    y  = tokens.count("Y")
    return n - rn - ar - 2 * y - 1


if __name__ == "__main__":
    rules, medicine = parse_input("i.txt")

    # Part 1
    molecules = distinct_molecules_after_one_step(rules, medicine)
    print("Part 1 - distinct molecules after one replacement:", len(molecules))

    # Part 2
    steps = steps_from_e_formula(medicine)
    print("Part 2 - fewest steps from 'e' to medicine:", steps)
