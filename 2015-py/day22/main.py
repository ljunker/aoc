import math

# Spells:
# Magic Missile: 53 mana, 4 damage
# Drain:         73 mana, 2 damage and +2 HP
# Shield:       113 mana, +7 armor for 6 turns
# Poison:       173 mana, 3 damage/turn for 6 turns
# Recharge:     229 mana, +101 mana/turn for 5 turns

PLAYER_START_HP = 50
PLAYER_START_MANA = 500

SPELLS = {
    "MagicMissile": {"cost": 53},
    "Drain":        {"cost": 73},
    "Shield":       {"cost": 113, "duration": 6},
    "Poison":       {"cost": 173, "duration": 6},
    "Recharge":     {"cost": 229, "duration": 5},
}


def read_boss(filename="i.txt"):
    hp = dmg = None
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
    if hp is None or dmg is None:
        raise ValueError("Boss stats not fully specified in i.txt")
    return hp, dmg


def apply_effects(player_hp, player_mana, boss_hp,
                  shield_timer, poison_timer, recharge_timer):
    """
    Apply all active effects at the start of a turn.
    - Poison damages the boss
    - Shield sets armor to 7 while active
    - Recharge adds mana
    Then decrement timers.
    Return new state and armor value for this turn.
    """
    armor = 7 if shield_timer > 0 else 0

    # Effects apply
    if poison_timer > 0:
        boss_hp -= 3
    if recharge_timer > 0:
        player_mana += 101

    # Timers tick down
    shield_timer = max(0, shield_timer - 1)
    poison_timer = max(0, poison_timer - 1)
    recharge_timer = max(0, recharge_timer - 1)

    return (player_hp, player_mana, boss_hp,
            shield_timer, poison_timer, recharge_timer, armor)


def search_min_mana_to_win(boss_hp, boss_damage, hard_mode=False):
    best = [math.inf]  # global best found so far

    def dfs(player_hp, player_mana, boss_hp,
            shield_timer, poison_timer, recharge_timer,
            mana_spent):
        # Prune: no need to continue if we already spent more than best
        if mana_spent >= best[0]:
            return

        # ---------- Player turn ----------
        # Hard mode: lose 1 HP at the start of every *player* turn
        if hard_mode:
            player_hp -= 1
            if player_hp <= 0:
                return  # dead before anything else

        # Apply effects at start of player turn
        (player_hp, player_mana, boss_hp,
         shield_timer, poison_timer, recharge_timer, armor) = apply_effects(
            player_hp, player_mana, boss_hp,
            shield_timer, poison_timer, recharge_timer
        )

        # Maybe poison killed the boss
        if boss_hp <= 0:
            best[0] = min(best[0], mana_spent)
            return

        # Try each spell
        for spell_name, info in SPELLS.items():
            cost = info["cost"]

            # Can't cast if we don't have enough mana
            if cost > player_mana:
                continue

            # Can't cast an already-active effect
            if spell_name == "Shield" and shield_timer > 0:
                continue
            if spell_name == "Poison" and poison_timer > 0:
                continue
            if spell_name == "Recharge" and recharge_timer > 0:
                continue

            # Copy state
            p_hp = player_hp
            p_mana = player_mana - cost
            b_hp = boss_hp
            s_t = shield_timer
            p_t = poison_timer
            r_t = recharge_timer
            new_mana_spent = mana_spent + cost

            # Apply immediate spell effects
            if spell_name == "MagicMissile":
                b_hp -= 4
            elif spell_name == "Drain":
                b_hp -= 2
                p_hp += 2
            elif spell_name == "Shield":
                s_t = SPELLS["Shield"]["duration"]
            elif spell_name == "Poison":
                p_t = SPELLS["Poison"]["duration"]
            elif spell_name == "Recharge":
                r_t = SPELLS["Recharge"]["duration"]

            # Did that kill the boss right away?
            if b_hp <= 0:
                best[0] = min(best[0], new_mana_spent)
                continue

            # ---------- Boss turn ----------
            (p_hp, p_mana, b_hp,
             s_t, p_t, r_t, armor2) = apply_effects(
                p_hp, p_mana, b_hp, s_t, p_t, r_t
            )

            # Maybe poison killed the boss on boss turn start
            if b_hp <= 0:
                best[0] = min(best[0], new_mana_spent)
                continue

            # Boss attacks
            damage_to_player = max(1, boss_damage - armor2)
            p_hp -= damage_to_player
            if p_hp <= 0:
                # Player dead, this branch is a loss
                continue

            # Recurse to next player turn
            dfs(p_hp, p_mana, b_hp, s_t, p_t, r_t, new_mana_spent)

    dfs(PLAYER_START_HP, PLAYER_START_MANA, boss_hp,
        shield_timer=0, poison_timer=0, recharge_timer=0,
        mana_spent=0)

    return best[0]


if __name__ == "__main__":
    boss_hp, boss_damage = read_boss("i.txt")

    part1 = search_min_mana_to_win(boss_hp, boss_damage, hard_mode=False)
    print("Part 1 - least mana to win (normal):", part1)

    part2 = search_min_mana_to_win(boss_hp, boss_damage, hard_mode=True)
    print("Part 2 - least mana to win (hard):", part2)
