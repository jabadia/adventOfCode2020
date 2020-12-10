import time
from functools import wraps

from utils.test_case import TestCase
from d10_input import INPUT

TEST_CASES = [
    TestCase("""
1
2
3
""", 4),
    TestCase("""
16
10
15
5
1
11
7
19
6
12
4
""", 8),
    TestCase("""
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
""", 19208)
]


def memoize(f):
    memo = {}

    @wraps(f)
    def helper(adapters, start):
        key = (tuple(adapters[:10]), start)
        if key not in memo:
            memo[key] = f(adapters, start)
        return memo[key]

    return helper


@memoize
def valid_arrangements(adapters, start):
    if start + 1 == len(adapters):
        return 1

    arrangements = 0
    for i in [1, 2, 3]:
        if start + i < len(adapters) and adapters[start + i] - adapters[start] <= 3:
            arrangements += valid_arrangements(adapters, start + i)

    return arrangements


assert valid_arrangements([0, 3, 6], 0) == 1
assert valid_arrangements([0, 2, 4, 6], 0) == 1
assert valid_arrangements([0, 1, 2, 3, 6], 0) == 4


def solve(input):
    adapters = [0] + sorted(int(n) for n in input.strip().split('\n'))
    adapters += [adapters[-1] + 3]

    return valid_arrangements(adapters, 0)


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
