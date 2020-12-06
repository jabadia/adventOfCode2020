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


def intersection(sets):
    first = next(sets)  # sets is a generator, we take the first element
    return first.intersection(*sets)


def solve(input):
    return sum(
        len(
            intersection(set(answers) for answers in group.split('\n'))
        ) for group in input.strip().split('\n\n')
    )


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    print(solve(INPUT))
