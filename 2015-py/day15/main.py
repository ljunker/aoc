import re

def parse_input(filename="i.txt"):
    """
    Parse lines like:
    Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
    """
    ingredients = []
    pattern = re.compile(
        r"(\w+): capacity (-?\d+), durability (-?\d+), "
        r"flavor (-?\d+), texture (-?\d+), calories (-?\d+)"
    )

    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = pattern.match(line)
            if not m:
                raise ValueError(f"Cannot parse line: {line}")
            name, cap, dur, fla, tex, cal = m.groups()
            ingredients.append({
                "name": name,
                "capacity": int(cap),
                "durability": int(dur),
                "flavor": int(fla),
                "texture": int(tex),
                "calories": int(cal),
            })
    return ingredients


def score_for_amounts(ingredients, amounts):
    """
    Given a list of ingredients and matching list of teaspoon amounts,
    compute the cookie score (ignoring calories).
    """
    cap = dur = fla = tex = 0
    for ing, amt in zip(ingredients, amounts):
        cap += ing["capacity"] * amt
        dur += ing["durability"] * amt
        fla += ing["flavor"] * amt
        tex += ing["texture"] * amt

    cap = max(cap, 0)
    dur = max(dur, 0)
    fla = max(fla, 0)
    tex = max(tex, 0)

    return cap * dur * fla * tex


def calories_for_amounts(ingredients, amounts):
    return sum(ing["calories"] * amt for ing, amt in zip(ingredients, amounts))


def search_best_score(ingredients, total_teaspoons=100, calorie_target=None):
    """
    Brute-force search:
      - total_teaspoons distributed across ingredients
      - if calorie_target is not None, only consider mixes with that many calories
    """
    n = len(ingredients)
    best = 0

    def backtrack(i, remaining, current_amounts):
        nonlocal best

        if i == n - 1:
            # Last ingredient gets the remaining teaspoons
            amounts = current_amounts + [remaining]

            if calorie_target is not None:
                if calories_for_amounts(ingredients, amounts) != calorie_target:
                    return

            s = score_for_amounts(ingredients, amounts)
            if s > best:
                best = s
            return

        # Distribute 0..remaining teaspoons to ingredient i
        for amt in range(remaining + 1):
            backtrack(i + 1, remaining - amt, current_amounts + [amt])

    backtrack(0, total_teaspoons, [])
    return best


if __name__ == "__main__":
    ingredients = parse_input("i.txt")

    # Part 1: no calorie constraint
    best_score_part1 = search_best_score(ingredients, total_teaspoons=100, calorie_target=None)
    print("Part 1 - best cookie score:", best_score_part1)

    # Part 2: exactly 500 calories
    best_score_part2 = search_best_score(ingredients, total_teaspoons=100, calorie_target=500)
    print("Part 2 - best cookie score with 500 calories:", best_score_part2)
