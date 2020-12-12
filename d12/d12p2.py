import re
import time
from collections import namedtuple

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

#     N
#     |
# W --+-- E
#     |
#     S

Vector = namedtuple('Vector', "x y")

DELTAS = {
    'N': Vector(0, 1),
    'E': Vector(1, 0),
    'S': Vector(0, -1),
    'W': Vector(-1, 0),
}


def rotate(point, side):
    if side == 'L':  # counter clockwise
        return Vector(-point.y, point.x)
    else:  # clockwise
        return Vector(point.y, -point.x)


def move(pos, delta, distance):
    return Vector(pos.x + delta.x * distance, pos.y + delta.y * distance)


def solve(input):
    pos = Vector(0, 0)
    waypoint = Vector(10, 1)
    for line in input.strip().split('\n'):
        instruction, distance = re.match('([NSEWLRF])(\d+)$', line).groups()
        distance = int(distance)
        if instruction in 'NSEW':
            waypoint = move(waypoint, DELTAS[instruction], distance)
        elif instruction == 'F':
            pos = move(pos, waypoint, distance)
        elif instruction in 'LR':
            angle = distance // 90
            for i in range(angle):
                waypoint = rotate(waypoint, instruction)

    return abs(pos.x) + abs(pos.y)


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
