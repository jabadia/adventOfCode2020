import time
from utils.test_case import TestCase
from d11_input import INPUT

TEST_CASES = [
    TestCase("""
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
""", 37),
]


def neighbours(ferry, row, col):
    occupied_seats = 0
    for i in range(max(row - 1, 0), min(len(ferry), row + 2)):
        for j in range(max(col - 1, 0), min(len(ferry[0]), col + 2)):
            if (i != row or j != col) and ferry[i][j] == '#':
                occupied_seats += 1
    return occupied_seats


test_ferry1 = [
    "LLL",
    "LLL",
    "LLL",
]

test_ferry2 = [
    "###",
    "LL#",
    "LLL",
]

# assert neighbours(test_ferry1, 1, 1) == 0
# assert neighbours(test_ferry1, 0, 0) == 0
# assert neighbours(test_ferry1, 2, 2) == 0

assert neighbours(test_ferry2, 1, 1) == 4
assert neighbours(test_ferry2, 0, 0) == 1
assert neighbours(test_ferry2, 2, 2) == 1


def next_generation(ferry):
    next_ferry = []
    rows = len(ferry)
    cols = len(ferry[0])
    for row in range(rows):
        next_row = []
        for col in range(cols):
            if ferry[row][col] == '.':
                next_row.append('.')
            elif ferry[row][col] == 'L':
                next_row.append('#' if neighbours(ferry, row, col) == 0 else 'L')
            elif ferry[row][col] == '#':
                next_row.append('#' if neighbours(ferry, row, col) < 4 else 'L')
        next_ferry.append(''.join(next_row))
    return next_ferry


def get_hash(ferry):
    return sum(i * sum(j for j, cell in enumerate(row) if cell == '#') for i, row in enumerate(ferry))


def solve(input):
    ferry = input.strip().split('\n')
    last_hash = None
    iteration = 0
    while True:
        ferry = next_generation(ferry)
        # print()
        # for row in ferry:
        #     print(row)
        hash = get_hash(ferry)
        if hash == last_hash:
            return sum(row.count('#') for row in ferry)
        last_hash = hash
        print(iteration, last_hash)
        iteration += 1


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
