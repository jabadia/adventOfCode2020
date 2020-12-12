import re
import time
from utils.test_case import TestCase
from d12_input import INPUT

TEST_CASES = [
    TestCase("""
F10
N3
F7
R90
F11
""", 286),
]

DIRECTION = {
    'N': 1j,
    'S': -1j,
    'E': 1,
    'W': -1,
}

TURN = {
    'L': 1j,
    'R': -1j,
}


def solve(input):
    pos = 0
    waypoint = 10 + 1j
    for line in input.strip().split('\n'):
        instruction, distance = re.match('([NSEWLRF])(\d+)$', line).groups()
        distance = int(distance)
        if instruction in 'NSEW':
            waypoint = waypoint + distance * DIRECTION[instruction]
        elif instruction == 'F':
            pos = pos + distance * waypoint
        elif instruction in 'LR':
            angle = distance // 90
            waypoint = waypoint * (TURN[instruction] ** angle)

    return abs(pos.real) + abs(pos.imag)


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
