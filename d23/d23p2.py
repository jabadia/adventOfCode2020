import re
import time

from utils.test_case import TestCase
from d23_input import INPUT
from collections import deque
from itertools import islice

TEST_CASES = [
    TestCase('389125467', '67384529'),
    TestCase('364289715', '98645732'),
    # TestCase('389125467', 149245887792)
]


def solve(input):
    cups = deque(int(d) for d in input.strip())
    min_cup = min(cups)
    max_cup = max(cups)

    for round in range(100):
        current_cup = cups.popleft()
        pick = [cups.popleft() for i in range(3)]
        cups.appendleft(current_cup)
        search_for = current_cup - 1
        while search_for in pick or search_for == 0:
            search_for -= 1
            if search_for < min_cup:
                search_for = max_cup
        destination_pos = cups.index(search_for)
        for p in reversed(pick):
            cups.insert(destination_pos + 1, p)
        cups.rotate(-1)
        # print(round, ''.join(str(cup) for cup in cups))

    cups.rotate(-cups.index(1))
    cups.popleft()
    return ''.join(str(cup) for cup in cups)


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
