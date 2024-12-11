with open("input.txt") as f:
    floor = 0
    count = 0
    for line in f:
        for i in line:
            if i == '(':
                floor += 1
            else:
                floor -= 1
            count += 1
            if floor == -1:
                print(count)