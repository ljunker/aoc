def parse_input(filename="i.txt"):
    reindeer = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Example:
            # "Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds."
            parts = line.split()
            name = parts[0]
            speed = int(parts[3])          # km/s
            fly_time = int(parts[6])       # seconds
            rest_time = int(parts[13])     # seconds

            reindeer.append((name, speed, fly_time, rest_time))
    return reindeer


def distance_after(speed, fly_time, rest_time, total_time):
    """Part 1: distance after total_time seconds."""
    cycle = fly_time + rest_time
    full_cycles = total_time // cycle
    remaining = total_time % cycle

    dist = full_cycles * speed * fly_time
    extra_fly = min(remaining, fly_time)
    dist += extra_fly * speed

    return dist


def simulate_points(herd, total_time):
    """Part 2: simulate race and return max points any reindeer gets."""
    # State per reindeer
    distances = {name: 0 for name, _, _, _ in herd}
    points = {name: 0 for name, _, _, _ in herd}

    for t in range(1, total_time + 1):
        # Update distances
        for name, speed, fly_time, rest_time in herd:
            cycle = fly_time + rest_time
            # (t-1) because at t=1 we're in the first second of the cycle
            phase = (t - 1) % cycle
            if phase < fly_time:
                distances[name] += speed

        # Find leaders
        lead_dist = max(distances.values())
        for name in distances:
            if distances[name] == lead_dist:
                points[name] += 1

    return max(points.values()), points


if __name__ == "__main__":
    TOTAL_TIME = 2503
    herd = parse_input("i.txt")

    # Part 1
    best_dist = 0
    best_name = None
    for name, speed, fly, rest in herd:
        d = distance_after(speed, fly, rest, TOTAL_TIME)
        if d > best_dist:
            best_dist = d
            best_name = name
    print("Part 1 - winning distance:", best_dist, "by", best_name)

    # Part 2
    best_points, all_points = simulate_points(herd, TOTAL_TIME)
    print("Part 2 - winning points:", best_points)
