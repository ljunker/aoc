import string

ALPH = string.ascii_lowercase
FORBIDDEN = set("iol")


def increment(pw: str) -> str:
    """
    Increment the password like a base-26 number (a..z),
    wrapping z -> a and carrying left.
    """
    pw_list = list(pw)
    i = len(pw_list) - 1

    while i >= 0:
        if pw_list[i] == 'z':
            pw_list[i] = 'a'
            i -= 1
        else:
            pw_list[i] = chr(ord(pw_list[i]) + 1)
            break

    return "".join(pw_list)


def has_straight(pw: str) -> bool:
    """Check for an increasing straight of at least three letters."""
    for i in range(len(pw) - 2):
        a, b, c = pw[i], pw[i + 1], pw[i + 2]
        if ord(b) == ord(a) + 1 and ord(c) == ord(b) + 1:
            return True
    return False


def has_no_forbidden(pw: str) -> bool:
    """Check password has no i, o, l."""
    return not any(ch in FORBIDDEN for ch in pw)


def has_two_pairs(pw: str) -> bool:
    """Check for at least two different non-overlapping pairs (aa, bb, ...)."""
    pairs = set()
    i = 0
    while i < len(pw) - 1:
        if pw[i] == pw[i + 1]:
            pairs.add(pw[i])
            i += 2  # skip over this pair to avoid overlap
        else:
            i += 1
    return len(pairs) >= 2


def is_valid(pw: str) -> bool:
    return has_straight(pw) and has_no_forbidden(pw) and has_two_pairs(pw)


def next_password(pw: str) -> str:
    pw = increment(pw)
    while not is_valid(pw):
        pw = increment(pw)
    return pw


if __name__ == "__main__":
    start = "hepxcrrq"
    part1 = next_password(start)
    print("Next valid password (Part 1):", part1)
    part2 = next_password(part1)
    print("Next valid password (Part 2):", part2)
