#!/bin/sh
set -e

usage() {
    echo "Usage: $0 YEAR DAY"
    echo "  Example: $0 2025 1 "
    exit 1
}

if [ $# -ne 2 ]; then
    usage
fi

YEAR="$1"
DAY="$2"

# Pad day to two digits
DAY_PADDED=$(printf "%02d" "$DAY")

DIR_NAME="${YEAR}-py/day${DAY_PADDED}"

FNAME="${DIR_NAME}/${YEAR}_day${DAY_PADDED}.py"

if [ -e "$FNAME" ]; then
    echo "Error: $FNAME already exists" >&2
    exit 1
fi

mkdir -p "$DIR_NAME"

cat >"$FNAME" <<EOF
from aocfw import AdventOfCodeClient

YEAR = ${YEAR}
DAY = ${DAY}


def part1(part_data):
    return 0


def part2(part_data):
    return 0


if __name__ == "__main__":
    client = AdventOfCodeClient()

    data = client.get_input(YEAR, DAY)
    answer = part1(data)
    print("Part 1:", answer)
    # res = client.submit_answer(YEAR, DAY, 1, answer)
    # print(res.message)

    answer = part2(data)
    print("Part 2:", answer)
    # res = client.submit_answer(YEAR, DAY, 2, answer)
    # print(res.message)

EOF

echo "Created $FNAME\n"
