from utils.test_case import TestCase
from d3_input import INPUT

TEST_CASES = [
    TestCase("""
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
""", 7)
]


def solve(input):
    forest = input.strip().split('\n')
    bottom = len(forest)
    width = len(forest[0])
    row, col = (1, 3)
    trees = 0
    while row < bottom:
        if forest[row][col % width] == '#':
            trees += 1
        row, col = (row + 1, col + 3)
    return trees


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    print(solve(INPUT))
