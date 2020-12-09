from collections import deque

from utils.test_case import TestCase
from d9_input import INPUT

TEST_CASES = [
    TestCase(("""
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    13
    14
    15
    16
    17
    18
    19
    29
    21
    22
    23
    24
    25
    26
    49
    100
    50
    """, 25), 100),
    TestCase(("""
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576    
""", 5), 127),
]


def sum_in_preamble(numbers, i, preamble_len):
    for p0 in range(i - preamble_len, i):
        for p1 in range(p0 + 1, i):
            if numbers[p0] + numbers[p1] == numbers[i]:
                return True
    return False


def solve(input, preamble_len):
    numbers = [int(n) for n in input.strip().split('\n')]
    for i in range(preamble_len, len(numbers) + 1):
        if not sum_in_preamble(numbers, i, preamble_len):
            return numbers[i]
    return None


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(*case.case)
        case.check(result)

    print(solve(INPUT, 25))
