import re

import numpy as np


class Moon:
    def __init__(self, l):
        match = re.search(r"=(-?\d+).*?=(-?\d+).*?=(-?\d+)", l)
        self.x = int(match.group(1))
        self.y = int(match.group(2))
        self.z = int(match.group(3))
        self.vx, self.vy, self.vz = 0, 0, 0
        self.configs = dict()

    def apply_gravity(self, ax, ay, az):
        self.vx += ax
        self.vy += ay
        self.vz += az

    def apply_velocity(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def pot(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def kin(self):
        return abs(self.vx) + abs(self.vy) + abs(self.vz)

    def check_config(self, i, conf):
        if conf in self.configs:
            return i - self.configs[conf]
        self.configs[conf] = i


def apply_gravity(m0, m1):
    ax = np.sign(m0.x - m1.x)
    ay = np.sign(m0.y - m1.y)
    az = np.sign(m0.z - m1.z)
    m0.apply_gravity(-ax, -ay, -az)


moons = [Moon(l) for l in open("sample.txt").readlines()]
configs = dict()
i = 0
x_rep, y_rep, z_rep = -1, -1, -1
xi = tuple(m.x for m in moons)
yi = tuple(m.y for m in moons)
zi = tuple(m.z for m in moons)
for i in range(10000000):
    [apply_gravity(m0, m1) for m0 in moons for m1 in moons if m0 != m1]
    [m.apply_velocity() for m in moons]
    xs = tuple(m.x for m in moons)
    ys = tuple(m.y for m in moons)
    zs = tuple(m.z for m in moons)
    if xs == xi:
        x_rep = i + 2 if x_rep == -1 else x_rep
    if ys == yi:
        y_rep = i + 2 if y_rep == -1 else y_rep
    if zs == zi:
        z_rep = i + 2 if z_rep == -1 else z_rep

    if x_rep != -1 and y_rep != -1 and z_rep != -1:
        break
print(np.lcm(np.lcm(x_rep, y_rep), z_rep))
