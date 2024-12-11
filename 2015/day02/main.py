with open("i.txt") as f:
    sum = 0
    ribbon = 0
    for line in f:
        dim = line.split("x")
        l = int(dim[0])
        w = int(dim[1])
        h = int(dim[2])
        a, b, c = l * w, w * h, h * l
        paper = 2 * (a + b + c)
        paper += min(a, b, c)
        print(paper)
        sum += paper
        cubic = l*w*h
        sorted = [l, w, h]
        sorted.sort()
        length = sorted[0]*2 + sorted[1]*2 + cubic
        ribbon += length
    print(sum)
    print(ribbon)
