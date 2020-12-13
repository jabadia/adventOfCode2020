import time

from utils.test_case import TestCase
from d13_input import INPUT

TEST_CASES = [
    TestCase("""
939
7,13,x,x,59,x,31,19
""", 295),
]


def solve(input):
    lines = input.strip().split('\n')
    start = int(lines[0])
    buses = [int(bus) for bus in lines[1].strip().split(',') if bus != 'x']
    wait, bus = min((bus - start % bus, bus) for bus in buses)
    return wait * bus


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
