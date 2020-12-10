import time
from utils.test_case import TestCase
from d10_input import INPUT

TEST_CASES = [
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
""", 7*5),
]


def solve(input):
    adapters = [0] + sorted(int(n) for n in input.strip().split('\n'))
    counts = {
        1: 0,
        2: 0,
        3: 0,
    }
    for i in range(1, len(adapters)):
        diff = adapters[i] - adapters[i-1]
        counts[diff] += 1

    return counts[1] * (1+counts[3])


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
