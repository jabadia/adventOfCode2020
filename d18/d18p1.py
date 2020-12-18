import time

from utils.test_case import TestCase
from d18_input import INPUT

TEST_CASES = [
    TestCase("1 + 2 * 3 + 4 * 5 + 6", 71),
    TestCase("1 + (2 * 3) + (4 * (5 + 6))", 51),
    TestCase("2 * 3 + (4 * 5)", 26),
    TestCase("5 + (8 * 3 + 9 + 3 * 4 * 3)", 437),
    TestCase("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240),
    TestCase("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632),
]

def expr(tokens):
    total = None
    operator = None
    while tokens:
        token = tokens.pop(0)
        if token == '*' or token == '+':
            operator = token
        elif token == ')':
            return total
        else:
            if token == '(':
                value = expr(tokens)
            else:
                value = int(token)
            if operator == '+':
                total += value
            elif operator == '*':
                total *= value
            else:
                total = value

    return total

def solve(input):
    return sum(
        expr(line.replace('(', ' ( ').replace(')',' ) ').replace('  ', ' ').strip().split(' '))
        for line in input.strip().split('\n')
    )


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
