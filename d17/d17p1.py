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


def neighbours(cell):
    for delta in NEIGHBOURS:
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
        for cell in world:
            seen.add(cell)
            count = sum(neighbour in world for neighbour in neighbours(cell))
            if count == 2 or count == 3:
                next_world.add(cell)
            for cell2 in neighbours(cell):
                if cell2 not in seen:
                    seen.add(cell2)
                    count = sum(neighbour in world for neighbour in neighbours(cell2))
                    if cell2 in world:  # is currently active
                        if count == 2 or count == 3:
                            next_world.add(cell2)
                    else:  # is currently not active
                        if count == 3:
                            next_world.add(cell2)
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
