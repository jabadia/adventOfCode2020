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


def find_nearest_from(ferry, pos, delta):
    rows = len(ferry)
    cols = len(ferry[0])
    neighbour = (pos[0] + delta[0], pos[1] + delta[1])
    while 0 <= neighbour[0] < rows and 0 <= neighbour[1] < cols and ferry[neighbour[0]][neighbour[1]] == '.':
        neighbour = (neighbour[0] + delta[0], neighbour[1] + delta[1])

    if 0 <= neighbour[0] < rows and 0 <= neighbour[1] < cols:
        return neighbour
    else:
        return None


def find_neighbours(ferry):
    neighbours = {}
    rows = len(ferry)
    cols = len(ferry[0])
    for row in range(rows):
        for col in range(cols):
            # search for nearest neighbour in each direction
            if ferry[row][col] == '.':
                continue

            key = (row, col)

            neighbours[key] = list(filter(None, [
                find_nearest_from(ferry, (row, col), delta)
                for delta in [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
            ]))


    return neighbours


def visible_seats(ferry, neighhbours, row, col):
    return sum(1 for i, j in neighhbours.get((row, col), []) if ferry[i][j] == '#')


def next_generation(ferry, neighbours):
    rows = len(ferry)
    cols = len(ferry[0])

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
        next_ferry.append(next_row)
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
    ferry = [list(row) for row in input.strip().split('\n')]
    last_hash = None
    iteration = 0
    neighbours = find_neighbours(ferry)
    while True:
        ferry = next_generation(ferry, neighbours)
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
