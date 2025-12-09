import math
import itertools


PLAYER_HP = 100


# Shop inventory
WEAPONS = [
    ("Dagger",      8,  4, 0),
    ("Shortsword", 10,  5, 0),
    ("Warhammer",  25,  6, 0),
    ("Longsword",  40,  7, 0),
    ("Greataxe",   74,  8, 0),
]

ARMORS = [
    ("None",        0, 0, 0),  # armor is optional
    ("Leather",    13, 0, 1),
    ("Chainmail",  31, 0, 2),
    ("Splintmail", 53, 0, 3),
    ("Bandedmail", 75, 0, 4),
    ("Platemail", 102, 0, 5),
]

RINGS = [
    ("None1",       0, 0, 0),  # allow 0–2 rings by including "no ring" placeholders
    ("None2",       0, 0, 0),
    ("Damage +1",  25, 1, 0),
    ("Damage +2",  50, 2, 0),
    ("Damage +3", 100, 3, 0),
    ("Defense +1", 20, 0, 1),
    ("Defense +2", 40, 0, 2),
    ("Defense +3", 80, 0, 3),
]


def read_boss(filename="i.txt"):
    hp = dmg = armor = None
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            name, value = line.split(":")
            name = name.strip()
            value = int(value.strip())
            if name == "Hit Points":
                hp = value
            elif name == "Damage":
                dmg = value
            elif name == "Armor":
                armor = value
    if hp is None or dmg is None or armor is None:
        raise ValueError("Boss stats not fully specified in i.txt")
    return hp, dmg, armor


def player_wins(player_hp, player_dmg, player_armor, boss_hp, boss_dmg, boss_armor):
    # Effective damage per turn
    p_dpt = max(1, player_dmg - boss_armor)
    b_dpt = max(1, boss_dmg - player_armor)

    turns_to_kill_boss = math.ceil(boss_hp / p_dpt)
    turns_to_kill_player = math.ceil(player_hp / b_dpt)

    return turns_to_kill_boss <= turns_to_kill_player


def all_loadouts():
    """
    Generate all valid item combinations:
      - exactly 1 weapon
      - 0 or 1 armor
      - 0 to 2 rings, but using the None1/None2 placeholders so we always pick exactly 2
        and then just sum everything (duplicates of "None" are fine).
    """
    for w in WEAPONS:
        for a in ARMORS:
            for r1, r2 in itertools.combinations(RINGS, 2):
                items = [w, a, r1, r2]
                cost = sum(i[1] for i in items)
                dmg = sum(i[2] for i in items)
                arm = sum(i[3] for i in items)
                yield cost, dmg, arm


if __name__ == "__main__":
    boss_hp, boss_dmg, boss_armor = read_boss("i.txt")

    min_cost_to_win = None
    max_cost_to_lose = 0

    for cost, dmg, arm in all_loadouts():
        if player_wins(PLAYER_HP, dmg, arm, boss_hp, boss_dmg, boss_armor):
            if min_cost_to_win is None or cost < min_cost_to_win:
                min_cost_to_win = cost
        else:
            if cost > max_cost_to_lose:
                max_cost_to_lose = cost

    print("Part 1 - least gold to win:", min_cost_to_win)
    print("Part 2 - most gold while still losing:", max_cost_to_lose)
