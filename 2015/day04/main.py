import hashlib

secretKey = "iwrupvqb"
number = 0
solved = False
while not solved:
    test = secretKey + str(number)
    result = hashlib.md5(bytes(test, 'UTF-8')).hexdigest()
    if result.startswith("000000"):
        solved = True
    else:
        number += 1
print(number)