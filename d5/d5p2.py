from utils.test_case import TestCase
from d5_input import INPUT

TEST_CASES = [
]


def get_boarding_pass_id(line):
    row = int(line[:7].replace('F', '0').replace('B', '1'), 2)
    col = int(line[-3:].replace('L', '0').replace('R', '1'), 2)
    return row * 8 + col


def solve(input):
    occuppied_seats = set(get_boarding_pass_id(line) for line in input.strip().split('\n'))
    min_seat, max_seat = min(occuppied_seats), max(occuppied_seats)
    for i in range(min_seat, max_seat + 1):
        if i not in occuppied_seats:
            return i


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    print(solve(INPUT))
