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
""", 10),
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


def solve(input):
    black = set()
    for line in input.strip().split('\n'):
        steps = line.replace('se', SE).replace('sw', SW).replace('nw', NW).replace('ne', NE).replace('e', E).replace(
            'w', W)
        pos = (0, 0, 0)
        for step in steps:
            pos = move(pos, DIRECTIONS[step])

        if pos in black:
            black.remove(pos)
        else:
            black.add(pos)

    return len(black)


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
