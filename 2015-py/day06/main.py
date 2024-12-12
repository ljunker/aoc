import re

w,h = 1000, 1000
grid = [[0 for x in range(w)] for y in range(h)]

pattern = r"^(toggle|turn on|turn off)\s+(\d+),\s*(\d+)\s+through\s+(\d+),\s*(\d+)"

with open("i.txt") as f:
    for line in f:
        match = re.search(pattern, line)
        if match:
            action, x1, y1, x2, y2 = match.group(1), *map(int, match.groups()[1:])
            #print(f"Action: {action}, x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2}")
            for x in range(x1, x2+1):
                for y in range(y1, y2 + 1):
                    if action == "toggle":
                        grid[x][y] += 2
                    if action == "turn on":
                        grid[x][y] += 1
                    if action == "turn off":
                        grid[x][y] -= 1
                        if grid[x][y] < 0:
                            grid[x][y] = 0
        else:
            print("No match")

s = 0
for x in range(w):
    for y in range(h):
        s += grid[x][y]
print(s)