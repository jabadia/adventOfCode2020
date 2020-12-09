from collections import deque

from utils.test_case import TestCase
from d9_input import INPUT

TEST_CASES = [
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
""", 127), 62),
]


def solve(input, target):
    numbers = [int(n) for n in input.strip().split('\n')]
    sum = 0
    preamble = deque()
    for i in range(0, len(numbers)):
        if sum == target:
            return min(preamble) + max(preamble)
        sum += numbers[i]
        preamble.append(numbers[i])
        while sum > target:
            discard = preamble.popleft()
            sum -= discard

    return None


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(*case.case)
        case.check(result)

    target = 776203571
    print(solve(INPUT, target))
