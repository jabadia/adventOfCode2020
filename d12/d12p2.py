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
    'N': (0, 1),
    'S': (0, -1),
    'E': (1, 0),
    'W': (-1, 0),
}


def move(pos, direction, distance):
    return pos[0] + distance * direction[0], pos[1] + distance * direction[1]


def solve(input):
    pos = (0, 0)
    waypoint = (10, 1)
    for line in input.strip().split('\n'):
        instruction, distance = re.match('([NSEWLRF])(\d+)$', line).groups()
        distance = int(distance)
        if instruction in 'NSEW':
            waypoint = move(waypoint, DIRECTION[instruction], distance)
        elif instruction == 'F':
            pos = move(pos, waypoint, distance)
        elif instruction in 'LR':
            angle = distance // 90
            if instruction == 'R':
                for i in range(angle):
                    waypoint = (waypoint[1], -waypoint[0])  # turn clockwise
            else:
                for i in range(angle):
                    waypoint = (-waypoint[1], waypoint[0])  # turn counter-clockwise

    return abs(pos[0]) + abs(pos[1])


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
