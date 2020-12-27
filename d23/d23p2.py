import re
import time

from utils.test_case import TestCase
from d23_input import INPUT

TEST_CASES = [
    TestCase('389125467', 149245887792),
]

ONE_MILLION = 1000000


def solve(input):
    initial_cups = [int(d) for d in input.strip()]

    next = [None] * (ONE_MILLION + 1)
    for cup, next_cup in zip(
            initial_cups + list(range(max(initial_cups) + 1, ONE_MILLION + 1)),
            initial_cups[1:] + list(range(max(initial_cups) + 1, ONE_MILLION + 1)) + [initial_cups[0]]):
        next[cup] = next_cup

    current_cup = initial_cups[0]

    for round in range(10 * ONE_MILLION):
        if round % ONE_MILLION == 0:
            print(round)
        pick = [next[current_cup], next[next[current_cup]], next[next[next[current_cup]]]]
        search_for = current_cup - 1
        while search_for in pick or search_for == 0:
            search_for -= 1
            if search_for < 1:
                search_for = ONE_MILLION
        after = next[search_for]
        next[current_cup] = next[pick[-1]]
        next[search_for] = pick[0]
        next[pick[-1]] = after
        current_cup = next[current_cup]

    return next[1] * next[next[1]]


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
