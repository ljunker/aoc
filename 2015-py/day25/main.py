import re

MOD = 33554393
MUL = 252533
START = 20151125


def parse_row_col(filename="i.txt"):
    """
    Extract row and column numbers from the input text.
    Works for texts that contain two integers, e.g.:
      'Enter the code at row 2981, column 3075.'
    """
    with open(filename) as f:
        text = f.read()
    nums = list(map(int, re.findall(r"\d+", text)))
    if len(nums) < 2:
        raise ValueError("Could not find row and column in input.")
    row, col = nums[0], nums[1]
    return row, col


def sequence_index(row, col):
    """
    Compute the 1-based index in the diagonal sequence
    for the cell at (row, col), given the pattern:

       (1,1) -> 1
       (2,1) -> 2
       (1,2) -> 3
       (3,1) -> 4
       (2,2) -> 5
       (1,3) -> 6
       ...

    Diagonal number d = row + col - 1.
    Total cells before diagonal d: (d-1)*d/2.
    Within diagonal d, cells are filled starting at (d,1) going up-right,
    so position within diagonal is (d - row + 1).
    """
    d = row + col - 1
    before = (d - 1) * d // 2
    within = d - row + 1
    return before + within  # 1-based index


def code_at(row, col):
    idx = sequence_index(row, col)
    steps = idx - 1  # first cell is START, so 0 steps for index 1
    # code_n = START * MUL^steps mod MOD
    factor = pow(MUL, steps, MOD)
    return (START * factor) % MOD


if __name__ == "__main__":
    row, col = parse_row_col("i.txt")
    result = code_at(row, col)
    print("Row:", row, "Col:", col)
    print("Code for that position:", result)
