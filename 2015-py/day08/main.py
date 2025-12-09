def memory_length(code_literal: str) -> int:
    s = code_literal[1:-1]

    length = 0
    i = 0
    while i < len(s):
        if s[i] == '\\':
            if i + 1 < len(s):
                esc = s[i + 1]
                if esc in ['\\', '"']:
                    length += 1
                    i += 2
                elif esc == 'x':
                    length += 1
                    i += 4
                else:
                    length += 1
                    i += 2
            else:
                length += 1
                i += 1
        else:
            length += 1
            i += 1

    return length


def encoded_length(code_literal: str) -> int:
    length = 2

    for ch in code_literal:
        if ch in ['\\', '"']:
            length += 2
        else:
            length += 1

    return length


if __name__ == '__main__':
    fname = "i.txt"
    with open(fname) as f:
        lines = f.readlines()
        total_mem_len = 0
        total_code_len = 0
        total_encoded_len = 0
        for line in lines:
            line = line.rstrip('\n\r')
            if not line:
                continue
            total_code_len += len(line)
            total_mem_len += memory_length(line)
            total_encoded_len += encoded_length(line)
        print("Part1: ", total_code_len - total_mem_len)
        print("Part2: ", total_encoded_len - total_code_len)