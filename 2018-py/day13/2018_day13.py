import time
from dataclasses import dataclass

from aocfw import AdventOfCodeClient

YEAR = 2018
DAY = 13

DIRECTIONS = {
    "^": (0, -1),
    "v": (0, 1),
    "<": (-1, 0),
    ">": (1, 0),
}
LEFT_TURN = {
    "^": "<",
    "<": "v",
    "v": ">",
    ">": "^",
}
RIGHT_TURN = {
    "^": ">",
    ">": "v",
    "v": "<",
    "<": "^",
}
SLASH_TURN = {
    "^": ">",
    ">": "^",
    "v": "<",
    "<": "v",
}
BACKSLASH_TURN = {
    "^": "<",
    "<": "^",
    "v": ">",
    ">": "v",
}
CART_TRACKS = {
    "^": "|",
    "v": "|",
    "<": "-",
    ">": "-",
}


@dataclass
class Cart:
    x: int
    y: int
    direction: str
    turn: int = 0
    active: bool = True

    @property
    def position(self):
        return self.x, self.y


def part1(part_data):
    x, y = first_crash(part_data)
    return f"{x},{y}"


def part2(part_data):
    x, y = last_cart(part_data)
    return f"{x},{y}"


def parse_tracks(part_data):
    tracks = {}
    carts = []

    for y, line in enumerate(part_data.rstrip("\n").splitlines()):
        for x, char in enumerate(line):
            if char in CART_TRACKS:
                carts.append(Cart(x, y, char))
                tracks[(x, y)] = CART_TRACKS[char]
            elif char != " ":
                tracks[(x, y)] = char

    return tracks, carts


def move(cart, tracks):
    dx, dy = DIRECTIONS[cart.direction]
    cart.x += dx
    cart.y += dy

    track = tracks[cart.position]

    if track == "/":
        cart.direction = SLASH_TURN[cart.direction]
    elif track == "\\":
        cart.direction = BACKSLASH_TURN[cart.direction]
    elif track == "+":
        if cart.turn == 0:
            cart.direction = LEFT_TURN[cart.direction]
        elif cart.turn == 2:
            cart.direction = RIGHT_TURN[cart.direction]
        cart.turn = (cart.turn + 1) % 3


def first_crash(part_data):
    tracks, carts = parse_tracks(part_data)

    while True:
        carts.sort(key=lambda cart: (cart.y, cart.x))
        occupied = {
            cart.position: cart
            for cart in carts
        }

        for cart in carts:
            del occupied[cart.position]
            move(cart, tracks)

            if cart.position in occupied:
                return cart.position

            occupied[cart.position] = cart


def last_cart(part_data):
    tracks, carts = parse_tracks(part_data)

    while len(carts) > 1:
        carts.sort(key=lambda cart: (cart.y, cart.x))
        occupied = {
            cart.position: cart
            for cart in carts
            if cart.active
        }

        for cart in carts:
            if not cart.active:
                continue

            del occupied[cart.position]
            move(cart, tracks)

            crashed = occupied.pop(cart.position, None)
            if crashed is None:
                occupied[cart.position] = cart
            else:
                cart.active = False
                crashed.active = False

        carts = [
            cart
            for cart in carts
            if cart.active
        ]

    return carts[0].position


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
