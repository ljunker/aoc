def look_and_say(s: str) -> str:
    """Produce the next term in the look-and-say sequence from s."""
    out = []
    n = len(s)
    i = 0

    while i < n:
        ch = s[i]
        j = i + 1
        # Count run length of the same digit
        while j < n and s[j] == ch:
            j += 1
        run_length = j - i
        out.append(str(run_length))
        out.append(ch)
        i = j

    return ''.join(out)


if __name__ == '__main__':
    s = "1113222113"  # your puzzle input

    # Part 1: 40 iterations
    s40 = s
    for _ in range(40):
        s40 = look_and_say(s40)
    print("Part 1 length after 40:", len(s40))

    # Part 2: 50 iterations (starting from original input again)
    s50 = s
    for _ in range(50):
        s50 = look_and_say(s50)
    print("Part 2 length after 50:", len(s50))