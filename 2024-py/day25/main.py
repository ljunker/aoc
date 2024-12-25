def parse_locks_and_keys(lks):
    locks = []
    keys = []
    for lk in lks:
        lk = lk.split("\n")
        if lk[0] == "#####":
            lock = [0] * len(lk[0])
            for j in range(1, len(lk)):
                for i, col in enumerate(lk[j]):
                    if col == '#':
                        lock[i] += 1
            locks.append(lock)
        else:
            key = [5] * len(lk[0])
            for j in range(1, len(lk)):
                for i, col in enumerate(lk[j]):
                    if col == '.':
                        key[i] -= 1
            keys.append(key)
    return locks, keys

lks = open("i.txt").read().split("\n\n")
locks, keys = parse_locks_and_keys(lks)

combinations = 0
for lock in locks:
    for key in keys:
        fits = True
        for i in range(len(lock)):
            fits = fits and (lock[i]+key[i] < 6)
        if fits:
            combinations += 1
print(combinations)