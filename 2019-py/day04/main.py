from collections import Counter


def is_valid_password(number, p2=False):
    str_num = str(number)

    if len(str_num) != 6:
        return 0

    has_adjacent = any(str_num[i] == str_num[i + 1] for i in range(len(str_num) - 1))
    if not has_adjacent:
        return 0

    never_decrease = all(str_num[i] <= str_num[i + 1] for i in range(len(str_num) - 1))
    if not never_decrease:
        return 0

    counts = Counter(str_num)
    has_isolated_pair = 2 in counts.values()

    if p2 and not has_isolated_pair:
        return 0

    return 1


min_range = 240298
max_range = 784956

passwords = range(min_range, max_range)
print(sum(is_valid_password(num) for num in passwords))
print(sum(is_valid_password(num, True) for num in passwords))
