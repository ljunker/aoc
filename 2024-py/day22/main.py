from collections import defaultdict

numbers = [int(num) for num in open("i.txt").readlines()]

mod = 16777216


def next_num(x):
    x = ((x * 64) ^ x) % 16777216
    x = ((x >> 5) ^ x) % 16777216
    x = ((x * 2048) ^ x) % 16777216
    return x


p1 = 0
allprices = defaultdict(int)
for _, n in enumerate(numbers):
    prices = {}
    p = []
    dif = []
    for _ in range(2000):
        price = int(str(n)[-1])
        p.append(price)
        if len(p) > 1:
            dif.append(p[-1] - p[-2])
        if len(dif) > 3:
            key = tuple(dif[-4:])
            if key not in prices:
                prices[key] = price
                allprices[key] += price
        n = next_num(n)
    p1 += n

p2 = allprices[max(allprices, key=allprices.get)]
print(p1, p2)
