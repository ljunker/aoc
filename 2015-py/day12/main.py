import json

def sum_numbers(x):
    """Recursively sum all numbers in a JSON structure.

    Part 2 rule:
      If x is a dict and any value == "red", ignore the entire dict.
    """
    if isinstance(x, int):
        return x

    if isinstance(x, list):
        return sum(sum_numbers(v) for v in x)

    if isinstance(x, dict):
        # If ANY value is "red", ignore whole object
        if "red" in x.values():
            return 0
        return sum(sum_numbers(v) for v in x.values())

    return 0  # ignore strings, booleans, None


if __name__ == "__main__":
    with open("i.txt") as f:
        data = json.load(f)
    print(sum_numbers(data))
