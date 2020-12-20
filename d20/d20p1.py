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


def rotate(tile):
    return Tile(
        tile.id,
        (tile.borders[RIGHT], tile.borders[BOTTOM], tile.borders[LEFT], tile.borders[TOP])
    )

assert rotate(Tile(1, (1,2,3,4))) == Tile(1, (2,3,4,1))


def flipx(tile):
    return Tile(
        tile.id,
        (flipped_side(tile.borders[TOP]), tile.borders[RIGHT], flipped_side(tile.borders[BOTTOM]), tile.borders[LEFT])
    )

assert flipx(Tile(1, (1,2,3,4))) == Tile(1, (int('1000000000',2),2,int('1100000000',2),4)), f'{flipx(Tile(1, (1,2,3,4)))}'


def flipy(tile):
    return Tile(
        tile.id,
        (tile.borders[TOP], flipped_side(tile.borders[RIGHT]), tile.borders[BOTTOM], flipped_side(tile.borders[LEFT]))
    )

assert flipy(Tile(1, (1,2,3,4))) == Tile(1, (1,int('0100000000',2),3,int('0010000000',2))), f'{flipx(Tile(1, (1,2,3,4)))}'


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


def gen_tile_variations(tile):
    for i in range(4):
        yield tile
        yield flipx(tile)
        yield flipy(tile)
        tile = rotate(tile)


def gen_tiles_variations(tiles):
    return product(*[gen_tile_variations(tile) for tile in tiles])


def gen_arrangements(tiles):
    # return [
    #     [tiles[id] for id in (1951, 2311, 3079, 2729, 1427, 2473, 2971, 1489, 1171)]
    # ]
    variations = []
    for tile in tiles.values():
        tile_variations = []
        for i in range(4):
            tile_variations += [tile, flipx(tile), flipy(tile)]
            tile = rotate(tile)
        variations.append(tile_variations)

    for arrangement in permutations(variations):
        for variation in product(*arrangement):
            yield variation


def is_valid_arrangement(arrangement, image_size):
    for row in range(image_size - 1):
        for col in range(image_size - 1):
            tile = arrangement[row * image_size + col]
            tile_on_right = arrangement[row * image_size + col + 1]
            tile_below = arrangement[(row + 1) * image_size + col]
            valid = (
                    tile.borders[RIGHT] == tile_on_right.borders[LEFT] and
                    tile.borders[BOTTOM] == tile_below.borders[TOP]
            )
            if not valid:
                return False
    return True


def arrange_puzzle(tiles, image_size):
    for i, arrangement in enumerate(gen_arrangements(tiles)):
        if i % 1000000 == 0:
            print(i)
        # assert len(arrangement) == image_size * image_size
        if is_valid_arrangement(arrangement, image_size):
            # return 4 corners
            return (
                arrangement[0].id,
                arrangement[image_size - 1].id,
                arrangement[(image_size - 1) * image_size].id,
                arrangement[(image_size - 1) * image_size + (image_size - 1)].id
            )


def fit(tile, left_tile, above_tile):
    return (
            (not above_tile or tile.borders[TOP] == above_tile.borders[BOTTOM]) and
            (not left_tile or tile.borders[LEFT] == left_tile.borders[RIGHT])
    )


def print_puzzle(puzzle, image_size):
    for i, tile in enumerate(puzzle):
        if i % image_size == 0:
            print()
        print(f'{tile.id:4} ', end='')

    print('\n-')


def check_puzzle(puzzle, tiles, image_size):
    # print_puzzle(puzzle, image_size)
    if not tiles:
        return puzzle

    left_tile = puzzle[-1] if puzzle and len(puzzle) % image_size != 0 else None
    above_tile = puzzle[-image_size] if len(puzzle) >= image_size else None
    for tile in list(tiles):
        if fit(tile, left_tile, above_tile):
            valid = check_puzzle(puzzle + [tile], tiles - {tile}, image_size)
            if valid:
                return valid

    return None


def fast_find_corners(tiles, image_size):
    x_borders = Counter(border for tile in tiles for side, border in enumerate(tile.borders) if side in [LEFT, RIGHT])
    y_borders = Counter(border for tile in tiles for side, border in enumerate(tile.borders) if side in [TOP, BOTTOM])
    is_possible = (
            list(x_borders.values()).count(1) == image_size * 2 and
            list(x_borders.values()).count(2) == (image_size - 1) * image_size and
            list(y_borders.values()).count(1) == image_size * 2 and
            list(y_borders.values()).count(2) == (image_size - 1) * image_size
    )
    return is_possible
        # # ttiles = [(sum(borders[border] for border in tile.borders), tile) for tile in tiles]
        # # corners = [tile.id for sum_borders, tile in sorted(ttiles)[:4]]
        # if sorted([sum(borders[border] for border in tile.borders) for tile in tiles]) == [6, 6, 6, 6, 7, 7, 7, 7, 8]:
        #     print(Counter(borders.values()).most_common())
        #     ttiles = [(sum(borders[border] for border in tile.borders), tile) for tile in tiles]
        #     corners = [tile.id for sum_borders, tile in sorted(ttiles)[:4]]
        #     print(corners)
        #     return corners
        #
        # # print(sorted([sum(borders[border] for border in tile.borders) for tile in tiles]))
        # # return tiles
        # return corners


def solve(input):
    tiles = []
    for tile_section in input.strip().split('\n\n'):
        # tiles.add(parse_tile(tile_section))
        tile = parse_tile(tile_section)
        # tiles[tile.id] = tile
        tiles.append(tile)

    all_borders = [border for tile in tiles for border in tile.borders] + [flipped_side(border) for tile in tiles for border in tile.borders]

    image_size = math.isqrt(len(tiles))

    assert len(all_borders) == 2 * (len(set(all_borders)) - image_size * 4)

    c = Counter(all_borders)

    image_borders = [border for border, count in c.items() if count == 1]
    assert(len(image_borders)) == 2 * image_size * 4

    prod = 1
    for tile in tiles:
        is_corner = 2 == len([border for border in tile.borders if border in image_borders])
        if is_corner:
            print(tile)
            prod *= tile.id


    return prod

    for i, variation in enumerate(gen_tiles_variations(tiles)):
        if i % 1000000 == 0:
            print(i // 10000000)
        if not fast_find_corners(variation, image_size):
            continue

        arrangement = check_puzzle([], set(variation), image_size)
        if arrangement:
            corners = (
                arrangement[0].id,
                arrangement[image_size - 1].id,
                arrangement[(image_size - 1) * image_size].id,
                arrangement[(image_size - 1) * image_size + (image_size - 1)].id
            )
            return math.prod(corners)

    # corners = next(filter(None, (fast_find_corners(variation, image_size) for variation in gen_tiles_variations(tiles))))

    # print(len(list(options)))
    # for variation in gen_tiles_variations(tiles):
    #     corners = fast_find_corners(variation, image_size)
    #     if corners:
    #         return math.prod(corners)

    # valid = make_puzzle([], tiles, image_size)
    # assert is_valid_arrangement(valid, image_size)
    # # corners = arrange_puzzle(tiles, image_size)

    return None


if __name__ == '__main__':
    for case in TEST_CASES[2:]:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
