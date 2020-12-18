import time

from utils.test_case import TestCase
from d18_input import INPUT

TEST_CASES = [
    TestCase("1 + 2 * 3 + 4 * 5 + 6", 231),
    TestCase("1 + (2 * 3) + (4 * (5 + 6))", 51),
    TestCase("2 * 3 + (4 * 5)", 46),
    TestCase("5 + (8 * 3 + 9 + 3 * 4 * 3)", 1445),
    TestCase("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 669060),
    TestCase("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 23340),

    TestCase("5 + 8 * ((8 + 6 * 7 * 2) + (4 * 2 + 9 * 5 * 5 * 7) * 7 + 5) * 8 + 7", 18476640),  # MAL
    TestCase("((8 + 6 * 7 * 2) + (4 * 2 + 9 * 5 * 5 * 7) * 7 + 5) * 8 + 7", 1421280),  # MAL
    TestCase("((((8 + 6) * 7 * 2) + (4 * (2 + 9) * 5 * 5 * 7)) * (7 + 5))", 94752),  # MAL
    TestCase("(((196) + (4 * (2 + 9) * 5 * 5 * 7)) * (12))", 94752),  # MAL

    TestCase("(196 + (4 * (11) * 175)) * 12", 94752),  # MAL
    TestCase("(196 + (4 * (11) * 175)) * 12", 94752),  # MAL
    TestCase("(196 + (4 * (11) * 175))", 7896),  # BIEN
    TestCase("(4 * (11) * 175)", 7700),  # BIEN
    TestCase("(196 + (7700)) * 12", 94752),  # BIEN

    TestCase("(4 * (2 + 9) * 5 * 5 * 7)", 7700),
    TestCase("(4 * 2 + 9 * 5 * 5 * 7)", 7700),
    TestCase("((196 + (4 * 11 * 5 * 5 * 7)) * (7 + 5))", 94752),  # BIEN
    TestCase("(7 + 5)", 12),
    TestCase("(((8 + 6) * 7 * 2) + (4 * (2 + 9) * 5 * 5 * 7))", 7896),
    TestCase("((14 * 7 * 2) + (4 * (2 + 9) * 5 * 5 * 7))", 7896),
]

"""
expression ::= factor * expression | factor
factor ::= term + factor | term
term::= ( expression ) | num
"""


def expr(tokens):
    v1 = factor(tokens)
    if not tokens:
        return v1

    token = tokens.pop(0)
    if token == '*':
        return v1 * expr(tokens)

    tokens.insert(0, token)
    return v1


def factor(tokens):
    v1 = term(tokens)
    if not tokens:
        return v1
    token = tokens.pop(0)
    if token == '+':
        return v1 + factor(tokens)

    tokens.insert(0, token)
    return v1


def term(tokens):
    token = tokens.pop(0)
    if token == '(':
        v = expr(tokens)
        if tokens:
            token = tokens.pop(0)
            assert token == ')'
        return v
    else:
        return int(token)


def top_level(line):
    tokens = line.replace('(', ' ( ').replace(')', ' ) ').replace('  ', ' ').strip().split(' ')
    result = expr(tokens)
    assert len(tokens) == 0, line
    return result


def solve(input):
    return sum(
        top_level(line)
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
