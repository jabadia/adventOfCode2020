import time
from collections import defaultdict

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
""", 26),
]


def find_neighbours(ferry):
    neighbours = defaultdict(list)
    rows = len(ferry)
    cols = len(ferry[0])
    for row in range(rows):
        for col in range(cols):
            # search for nearest neighbour in each direction
            if ferry[row][col] == '.':
                continue

            key = (row, col)
            # north
            i = row - 1
            while i >= 0 and ferry[i][col] == '.':
                i -= 1
            if i >= 0:
                neighbours[key].append((i, col))
            # south
            i = row + 1
            while i < rows and ferry[i][col] == '.':
                i += 1
            if i < rows:
                neighbours[key].append((i, col))
            # west
            j = col - 1
            while j >= 0 and ferry[row][j] == '.':
                j -= 1
            if j >= 0:
                neighbours[key].append((row, j))
            # east
            j = col + 1
            while j < cols and ferry[row][j] == '.':
                j += 1
            if j < cols:
                neighbours[key].append((row, j))

            # diagonal NW
            i, j = row - 1, col - 1
            while i >= 0 and j >= 0 and ferry[i][j] == '.':
                i -= 1
                j -= 1
            if i >= 0 and j >= 0:
                neighbours[key].append((i, j))

            # diagonal SW
            i, j = row + 1, col - 1
            while i < rows and j >= 0 and ferry[i][j] == '.':
                i += 1
                j -= 1
            if i < rows and j >= 0:
                neighbours[key].append((i, j))

            # diagonal NE
            i, j = row - 1, col + 1
            while i >= 0 and j < cols and ferry[i][j] == '.':
                i -= 1
                j += 1
            if i >= 0 and j < cols:
                neighbours[key].append((i, j))

            # diagonal SE
            i, j = row + 1, col + 1
            while i < rows and j < cols and ferry[i][j] == '.':
                i += 1
                j += 1
            if i < rows and j < cols:
                neighbours[key].append((i, j))

    return dict(neighbours)


def visible_seats(ferry, neighhbours, row, col):
    return sum(1 for i, j in neighhbours.get((row, col), []) if ferry[i][j] == '#')


def next_generation(ferry, neighbours):
    rows = len(ferry)
    cols = len(ferry[0])
    # visible_seats = [[0] * cols for _ in range(rows)]
    # for row in range(rows):
    #     for col in range(cols):
    #         if ferry[row][col] != '#':
    #             continue
    #         # increment row
    #         for j in range(0, cols):
    #             visible_seats[row][j] += 1
    #         # increment col
    #         for i in range(0, rows):
    #             visible_seats[i][col] += 1
    #         # increment diagonals
    #         for i in range(0, rows):
    #             j1 = i - row + col
    #             if 0 <= j1 < cols:
    #                 visible_seats[i][j1] += 1
    #             j2 = col - (i - row)
    #             if 0 <= j2 < cols:
    #                 visible_seats[i][j2] += 1
    #         visible_seats[row][col] -= 4
    #
    # if test:
    #     test_row, test_col, expected_visible = test
    #     assert visible_seats[test_row][test_col] == expected_visible

    next_ferry = []
    for row in range(rows):
        next_row = []
        for col in range(cols):
            if ferry[row][col] == '.':
                next_row.append('.')
            elif ferry[row][col] == 'L':
                next_row.append('#' if visible_seats(ferry, neighbours, row, col) == 0 else 'L')
            elif ferry[row][col] == '#':
                next_row.append('#' if visible_seats(ferry, neighbours, row, col) < 5 else 'L')
        next_ferry.append(''.join(next_row))
    return next_ferry


def test_visible(ferry, row, col, expected_visible):
    neighbours = find_neighbours(ferry)
    actual_visible = visible_seats(ferry, neighbours, row, col)
    assert actual_visible == expected_visible
    print('ok')

test_visible([
    ".......#.",
    "...#.....",
    ".#.......",
    ".........",
    "..#L....#",
    "....#....",
    ".........",
    "#........",
    "...#.....",
], 4, 3, 8)

test_visible([
    ".............",
    ".L.L.#.#.#.#.",
    ".............",
], 1, 1, 0)

test_visible([
    ".##.##.",
    "#.#.#.#",
    "##...##",
    "...L...",
    "##...##",
    "#.#.#.#",
    ".##.##.",
], 3, 3, 0)


def get_hash(ferry):
    return sum(i * sum(j for j, cell in enumerate(row) if cell == '#') for i, row in enumerate(ferry))


def solve(input):
    ferry = input.strip().split('\n')
    last_hash = None
    iteration = 0
    neighbours = find_neighbours(ferry)
    while True:
        ferry = next_generation(ferry, neighbours)
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
