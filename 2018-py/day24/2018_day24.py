import re
import time
from dataclasses import dataclass, replace
from itertools import count

from aocfw import AdventOfCodeClient

YEAR = 2018
DAY = 24

IMMUNE_SYSTEM = "Immune System"
GROUP_PATTERN = re.compile(
    r"(\d+) units each with (\d+) hit points (?:\(([^)]+)\) )?"
    r"with an attack that does (\d+) (\w+) damage at initiative (\d+)"
)


@dataclass(eq=False)
class Group:
    army: str
    units: int
    hit_points: int
    attack: int
    attack_type: str
    initiative: int
    weaknesses: set[str]
    immunities: set[str]

    @property
    def power(self):
        return self.units * self.attack

    def damage_to(self, target):
        if self.attack_type in target.immunities:
            return 0
        return self.power * (2 if self.attack_type in target.weaknesses else 1)


def parse_groups(data):
    groups = []
    for block in data.strip().split("\n\n"):
        header, *lines = block.splitlines()
        for line in lines:
            match = GROUP_PATTERN.fullmatch(line)
            if match is None:
                raise ValueError(f"Invalid group: {line}")
            units, hit_points, traits, attack, attack_type, initiative = match.groups()
            resistances = {}
            if traits:
                for trait in traits.split("; "):
                    kind, types = trait.split(" to ")
                    resistances[kind] = set(types.split(", "))
            groups.append(Group(
                header.removesuffix(":"), int(units), int(hit_points), int(attack),
                attack_type, int(initiative), resistances.get("weak", set()),
                resistances.get("immune", set()),
            ))
    return groups


def fight(initial_groups, boost=0):
    groups = [
        replace(group, attack=group.attack + (boost if group.army == IMMUNE_SYSTEM else 0))
        for group in initial_groups
    ]
    while len({group.army for group in groups}) > 1:
        targets = {}
        reserved = set()
        for group in sorted(groups, key=lambda group: (group.power, group.initiative), reverse=True):
            candidates = (
                target for target in groups if target.army != group.army and target not in reserved
            )
            target = max(
                candidates,
                key=lambda target: (group.damage_to(target), target.power, target.initiative),
                default=None,
            )
            if target is not None and group.damage_to(target):
                targets[group] = target
                reserved.add(target)

        losses = 0
        for group in sorted(targets, key=lambda group: group.initiative, reverse=True):
            target = targets[group]
            killed = min(target.units, group.damage_to(target) // target.hit_points)
            target.units -= killed
            losses += killed
        if losses == 0:
            return None, 0
        groups = [group for group in groups if group.units]

    return groups[0].army, sum(group.units for group in groups)


def part1(part_data):
    winner, units = fight(parse_groups(part_data))
    if winner is None:
        raise ValueError("Battle ended in a stalemate")
    return units


def part2(part_data):
    groups = parse_groups(part_data)
    # A boost can change target selection, so test boosts in increasing order.
    for boost in count():
        winner, units = fight(groups, boost)
        if winner == IMMUNE_SYSTEM:
            return units


if __name__ == "__main__":
    client = AdventOfCodeClient()

    data = client.get_input(YEAR, DAY)
    answer = part1(data)
    print("Part 1:", answer)
    res = client.submit_answer(YEAR, DAY, 1, answer)
    print(res.message)

    time.sleep(10)

    answer = part2(data)
    print("Part 2:", answer)
    res = client.submit_answer(YEAR, DAY, 2, answer)
    print(res.message)
