from utils.test_case import TestCase
from d5_input import INPUT

TEST_CASES = [
    TestCase("""FBFBBFFRLR""", 357),  # (44, 5)
    TestCase("""BFFFBBFRRR""", 567),
    TestCase("""FFFBBBFRRR""", 119),
    TestCase("""BBFFBBFRLL""", 820)
]


def get_boarding_pass_id(line):
    row = int(line[:7].replace('F', '0').replace('B', '1'), 2)
    col = int(line[-3:].replace('L', '0').replace('R', '1'), 2)
    return row * 8 + col


def solve(input):
    return max(get_boarding_pass_id(line) for line in input.strip().split('\n'))


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    print(solve(INPUT))
