import math
import re
import time
from collections import namedtuple, Counter
from itertools import permutations, product

from utils.test_case import TestCase
from d20_input import INPUT

TEST_CASES = [
    TestCase("""
    Tile 1951:
    #...##.#..
    ..#.#..#.#
    .###....#.
    ###.##.##.
    .###.#####
    .##.#....#
    #...######
    .....#..##
    #.####...#
    #.##...##.

    Tile 2311:
    ..###..###
    ###...#.#.
    ..#....#..
    .#.#.#..##
    ##...#.###
    ##.##.###.
    ####.#...#
    #...##..#.
    ##..#.....
    ..##.#..#.

    Tile 3079:
    #.#.#####.
    .#..######
    ..#.......
    ######....
    ####.#..#.
    .#...#.##.
    #.#####.##
    ..#.###...
    ..#.......
    ..#.###...

    Tile 2729:
    #.##...##.
    ##..#.##..
    ##.####...
    ####.#.#..
    .#.####...
    .##..##.#.
    ....#..#.#
    ..#.#.....
    ####.#....
    ...#.#.#.#

    Tile 1427:
    ..##.#..#.
    ..#..###.#
    .#.####.#.
    ...#.#####
    ...##..##.
    ....#...##
    #.#.#.##.#
    .#.##.#..#
    .#..#.##..
    ###.##.#..

    Tile 2473:
    ..#.###...
    ##.##....#
    ..#.###..#
    ###.#..###
    .######.##
    #.#.#.#...
    #.###.###.
    #.###.##..
    .######...
    .##...####

    Tile 2971:
    ...#.#.#.#
    ..#.#.###.
    ..####.###
    #..#.#..#.
    .#..####.#
    .#####..##
    ##.##..#..
    #.#.###...
    #...###...
    ..#.#....#

    Tile 1489:
    ###.##.#..
    ..##.##.##
    ##.#...##.
    ...#.#.#..
    #..#.#.#.#
    #####...#.
    ..#...#...
    .##..##...
    ..##...#..
    ##.#.#....

    Tile 1171:
    .##...####
    #..#.##..#
    .#.#..#.##
    .####.###.
    ####.###..
    .##....##.
    .####...#.
    .####.##.#
    ...#..####
    ...##.....    
        """, 20899048083289),
    TestCase("""
Tile 2311:
..###..###
###...#.#.
..#....#..
.#.#.#..##
##...#.###
##.##.###.
####.#...#
#...##..#.
##..#.....
..##.#..#.

Tile 1951:
#...##.#..
..#.#..#.#
.###....#.
###.##.##.
.###.#####
.##.#....#
#...######
.....#..##
#.####...#
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...

Tile 2729:
#.##...##.
##..#.##..
##.####...
####.#.#..
.#.####...
.##..##.#.
....#..#.#
..#.#.....
####.#....
...#.#.#.#

Tile 1427:
..##.#..#.
..#..###.#
.#.####.#.
...#.#####
...##..##.
....#...##
#.#.#.##.#
.#.##.#..#
.#..#.##..
###.##.#..

Tile 2473:
..#.###...
##.##....#
..#.###..#
###.#..###
.######.##
#.#.#.#...
#.###.###.
#.###.##..
.######...
.##...####

Tile 2971:
...#.#.#.#
..#.#.###.
..####.###
#..#.#..#.
.#..####.#
.#####..##
##.##..#..
#.#.###...
#...###...
..#.#....#

Tile 1489:
###.##.#..
..##.##.##
##.#...##.
...#.#.#..
#..#.#.#.#
#####...#.
..#...#...
.##..##...
..##...#..
##.#.#....

Tile 1171:
.##...####
#..#.##..#
.#.#..#.##
.####.###.
####.###..
.##....##.
.####...#.
.####.##.#
...#..####
...##.....    
        """, 20899048083289),
    TestCase("""
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...    
""", 20899048083289)
]

# 1951    2311    3079
# 2729    1427    2473
# 2971    1489    1171

# (1951, 2311, 3079, 2729, 1427, 2473, 2971, 1489, 1171)

Tile = namedtuple('Tile', 'id borders')


def border_to_int(border):
    return int(border.replace('.', '0').replace('#', '1'), 2)


TOP = 0
RIGHT = 1
BOTTOM = 2
LEFT = 3


def pad(s):
    return '0' * (10 - len(s)) + s


def flipped_side(n):
    return int(pad(bin(n)[2:])[::-1], 2)


def parse_tile(tile_src):
    tile_lines = [line.strip() for line in tile_src.strip().split('\n')]
    id = int(re.match(r'Tile (\d+):', tile_lines[0]).group(1))
    top_border = border_to_int(tile_lines[1])
    bottom_border = border_to_int(tile_lines[-1])
    left_border = border_to_int(''.join(tile_lines[i][0] for i in range(1, len(tile_lines))))
    right_border = border_to_int(''.join(tile_lines[i][-1] for i in range(1, len(tile_lines))))
    tile = Tile(id, (top_border, right_border, bottom_border, left_border))
    assert all(len(tile_lines[i]) == 10 for i in range(1, len(tile_lines)))
    return tile


def solve(input):
    tiles = []
    for tile_section in input.strip().split('\n\n'):
        tile = parse_tile(tile_section)
        tiles.append(tile)

    image_size = math.isqrt(len(tiles))

    all_borders = (
            [border for tile in tiles for border in tile.borders] +
            [flipped_side(border) for tile in tiles for border in tile.borders]
    )

    # all borders are unique, and the outer borders appear only once
    assert len(all_borders) == 2 * (len(set(all_borders)) - image_size * 4)

    border_count = Counter(all_borders)

    outer_borders = [border for border, count in border_count.items() if count == 1]
    assert (len(outer_borders)) == 2 * image_size * 4  # because they may be flipped

    # one tile is a corner if it has 2 outer borders
    corners = [
        tile.id
        for tile in tiles
        if 2 == len([border for border in tile.borders if border in outer_borders])
    ]

    return math.prod(corners)


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
