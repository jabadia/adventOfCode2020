import time
import math

from utils.test_case import TestCase
from d13_input import INPUT

TEST_CASES = [
    TestCase("17,x,13,19", 3417),
    TestCase("7,13,x,x,59,x,31,19", 1068781),
    TestCase("67,7,59,61", 754018),
    TestCase("67,x,7,59,61", 779210),
    TestCase("67,7,x,59,61", 1261476),
    TestCase("1789,37,47,1889", 1202161486),
]


def solve_congruency(a, r, m):
    for i in range(1, m + 1):
        if (a * i) % m == r:
            return i
    return None


assert solve_congruency(494, 0, 17) == 17
assert solve_congruency(4199, 1, 2) == 1
assert solve_congruency(646, 11, 13) == 7
assert solve_congruency(442, 16, 19) == 7


def chinese_reminder_theorem_solution(buses):
    # http://matesup.cl/portal/revista/2007/4.pdf
    m = [bus for r, bus in buses]
    r = [r for r, bus in buses]
    M = math.prod(m)
    Mi = [M // mi for mi in m]
    u = [solve_congruency(Mii, 1, mi) for Mii, mi in zip(Mi, m)]
    time = sum(Mii * ui * ri for Mii, ui, ri in zip(Mi, u, r)) % M
    # print(f'M={M}')
    # print(f'M={Mi}')
    # print(f'r={r}')
    # print(f'u={u}')
    # print(f'time={time}')
    return time


# check that the implementation solves the example in the article http://matesup.cl/portal/revista/2007/4.pdf
# (pag 40, solución 2)
assert 23 == chinese_reminder_theorem_solution([(2, 3), (3, 5), (2, 7)])


def solve(input):
    buses = [
        ((-i) % int(bus), int(bus))
        for i, bus in enumerate(input.strip().split(','))
        if bus != 'x'
    ]
    return chinese_reminder_theorem_solution(buses)


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT.strip().split('\n')[1]))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
