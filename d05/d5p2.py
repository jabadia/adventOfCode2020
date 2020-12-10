from utils.test_case import TestCase
import re
from d5_input import INPUT

TEST_CASES = [
]


def get_boarding_pass_id(line):
    return int(re.sub(r'[BR]', '1', re.sub(r'[FL]', '0', line)), 2)


def solve(input):
    occuppied_seats = set(get_boarding_pass_id(line) for line in input.strip().split('\n'))
    free = None
    for seat in occuppied_seats:
        if seat + 1 not in occuppied_seats:
            if free:
                return min(free, seat + 1)
            else:
                free = seat + 1


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    print(solve(INPUT))
