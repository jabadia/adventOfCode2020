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
""", 336)
]


def solve(input):
    forest = input.strip().split('\n')
    bottom = len(forest)
    width = len(forest[0])
    product = 1
    for down, right in [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]:
        row, col = down, right
        trees = 0
        while row < bottom:
            if forest[row][col % width] == '#':
                trees += 1
            row, col = (row + down, col + right)
        product *= trees
    return product


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    print(solve(INPUT))
