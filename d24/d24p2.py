import re
import time

from utils.test_case import TestCase
from d24_input import INPUT

TEST_CASES = [
    TestCase("""
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
""", 2208),
]

E = '1'
SE = '2'
SW = '3'
W = '4'
NW = '5'
NE = '6'

DIRECTIONS = {
    E: (+1, -1, 0),
    SE: (0, -1, +1),
    SW: (-1, 0, +1),
    W: (-1, +1, 0),
    NW: (0, +1, -1),
    NE: (+1, 0, -1),
}


# https://www.redblobgames.com/grids/hexagons/#coordinates-cube

def move(pos, step):
    new_pos = (pos[0] + step[0], pos[1] + step[1], pos[2] + step[2])
    assert sum(new_pos) == 0
    return new_pos


BLOCK = 1
NEIGHBOURS = 2


def neighbours(tile, mode):
    if mode == BLOCK:
        yield tile
    for delta in DIRECTIONS.values():
        yield tile[0] + delta[0], tile[1] + delta[1], tile[2] + delta[2]


def next_gen(black):
    seen = set()
    next_black = set()
    for tile in black:
        for nearby_tile in neighbours(tile, BLOCK):
            if nearby_tile in seen:
                continue
            seen.add(nearby_tile)
            count = sum(neighbour in black for neighbour in neighbours(nearby_tile, NEIGHBOURS))
            if (nearby_tile in black and 1 <= count <= 2) or (nearby_tile not in black and count == 2):
                next_black.add(nearby_tile)
    return next_black


def solve(input):
    black = set()
    for line in input.strip().split('\n'):
        steps = (line
            .replace('se', SE).replace('sw', SW)
            .replace('nw', NW).replace('ne', NE)
            .replace('e', E).replace('w', W)
        )
        pos = (0, 0, 0)
        for step in steps:
            pos = move(pos, DIRECTIONS[step])

        if pos in black:
            black.remove(pos)
        else:
            black.add(pos)

    for i in range(100):
        black = next_gen(black)
        print(i, len(black))

    return len(black)


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
