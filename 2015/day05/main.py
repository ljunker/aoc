import re


def hasThreeVowels(l: str):
    vowels = "aeiouAEIOU"
    count = sum(1 for c in l if c in vowels)
    return count >= 3


def hasDouble(l):
    for i in range(len(l) - 1):
        if l[i] == l[i + 1]:
            return True
    return False


def badStrings(l):
    substrings = ["ab", "cd", "pq", "xy"]
    return any(substring in l for substring in substrings)


def check(l):
    if not hasThreeVowels(l):
        return 0
    if not hasDouble(l):
        return 0
    if badStrings(l):
        return 0
    return 1


def contains_rep_pair(l):
    return bool(re.search(r"(..).*\1", l))


def contains_repeating_letter_with_gap(l):
    return bool(re.search(r"(.).\1", l))


def check2(l):
    if not contains_rep_pair(l):
        return 0
    if not contains_repeating_letter_with_gap(l):
        return 0
    return 1


with open("i.txt") as f:
    s = 0
    for l in f:
        s += check2(l)
    print(s)
