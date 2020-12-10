from utils.test_case import TestCase
from d6_input import INPUT

TEST_CASES = [
    TestCase("""
abcx
abcy
abcz
""", 6),
]


def solve(input):
    return sum(len(set(group.replace('\n', ''))) for group in input.strip().split('\n\n'))


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    print(solve(INPUT))
