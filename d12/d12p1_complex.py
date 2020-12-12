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
""", 25),
]

TURN_LEFT = 1j
TURN_RIGHT = -1j

DIRECTION = {
    'N': 1j,
    'S': -1j,
    'E': 1,
    'W': -1,
}


def move(pos, direction, distance):
    return pos + distance * direction


def solve(input):
    pos = 0
    dir = DIRECTION['E']
    for line in input.strip().split('\n'):
        instruction, distance = re.match('([NSEWLRF])(\d+)$', line).groups()
        distance = int(distance)
        if instruction in 'NSEW':
            pos = move(pos, DIRECTION[instruction], distance)
        elif instruction == 'F':
            pos = move(pos, dir, distance)
        elif instruction in 'LR':
            angle = distance // 90
            turn = TURN_LEFT if instruction == 'L' else TURN_RIGHT
            dir = dir * (turn ** angle)

    return abs(pos.real) + abs(pos.imag)


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
