import time

from utils.test_case import TestCase
from d17_input import INPUT

TEST_CASES = [
    TestCase("""
.#.
..#
###
""", 112),
]

NEIGHBOURS = [(i, j, k) for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (-1, 0, 1) if not i == j == k == 0]
BLOCK = NEIGHBOURS + [(0, 0, 0)]

def neighbours(cell, deltas):
    for delta in deltas:
        yield (cell[0] + delta[0], cell[1] + delta[1], cell[2] + delta[2])


def solve(input):
    world = set()
    for i, row in enumerate(input.strip().split('\n')):
        for j, cell in enumerate(row):
            if cell == '#':
                world.add((i, j, 0))

    for cycle in range(6):
        seen = set()
        next_world = set()
        for active_cell in world:
            for nearby_cell in neighbours(active_cell, BLOCK):
                if nearby_cell in seen:
                    continue
                seen.add(nearby_cell)
                count = sum(neighbour in world for neighbour in neighbours(nearby_cell, NEIGHBOURS))
                if count == 3 or (count == 2 and nearby_cell in world):
                    next_world.add(nearby_cell)
        world = next_world

    return len(world)


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
