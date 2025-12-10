import hashlib

from aocfw import AdventOfCodeClient

YEAR = 2016
DAY = 5


def hash_it(data, idx):
    md5 = hashlib.md5()
    md5.update((data+str(idx)).encode())
    return md5.hexdigest()

def part1(part_data):
    idy = 0
    password = ''
    for _ in range(8):
        hash = hash_it(part_data, idy)
        while hash[:5] != '00000':
            idy += 1
            hash = hash_it(part_data, idy)
        idy += 1
        password += hash[5]
    return password

def part2(part_data):
    idy = 0
    password = ['-','-','-','-','-','-','-','-']
    while True:
        hash = hash_it(part_data, idy)
        while hash[:5] != '00000':
            idy += 1
            hash = hash_it(part_data, idy)
        idy += 1
        pos = hash[5]
        val = hash[6]
        try:
            if password[int(pos)] == '-':
                password[int(pos)] = val
                print(''.join(password))
        except:
            continue
        if '-' not in password:
            return ''.join(password)


if __name__ == "__main__":
    client = AdventOfCodeClient()

    data = client.get_input(YEAR, DAY)
    # answer = part1(data)
    # print("Part 1:", answer)
    # res = client.submit_answer(YEAR, DAY, 1, answer)
    # print(res.message)

    answer = part2(data)
    print("Part 2:", answer)
    # res = client.submit_answer(YEAR, DAY, 2, answer)
    # print(res.message)
