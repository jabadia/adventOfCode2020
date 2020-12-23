import re
import time

from utils.test_case import TestCase
from d23_input import INPUT

TEST_CASES = [
    TestCase('389125467', '67384529'),
]


def solve(input):
    cups = [int(d) for d in input.strip()]
    min_cup = min(cups)
    max_cup = max(cups)

    for round in range(100):
        current_cup = cups[0]
        pick = cups [1:4]
        cups = [cups[0]] + cups[4:]
        search_for = current_cup - 1
        while search_for not in cups:
            search_for -= 1
            if search_for < min_cup:
                search_for = max_cup
        destination_pos = cups.index(search_for)
        cups = cups[:destination_pos+1] + pick + cups[destination_pos+1:]
        cups = cups[1:] + cups[:1]

    start = cups.index(1)
    cups = cups[start+1:] + cups[:start]
    return ''.join(str(cup) for cup in cups)


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
