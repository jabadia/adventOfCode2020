from utils.test_case import TestCase
from d6_input import INPUT

TEST_CASES = [
    TestCase("""
abc

a
b
c

ab
ac

a
a
a
a

b
""", 6),
]


def solve(input):
    sum = 0
    for group in input.strip().split('\n\n'):
        common_answers = None
        for line in group.split('\n'):
            answers = set(line)
            if common_answers is not None:
                common_answers = common_answers.intersection(answers)
            else:
                common_answers = answers
        sum += len(common_answers)
    return sum


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    print(solve(INPUT))
