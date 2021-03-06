import math
import re
import time
from collections import namedtuple, Counter
from itertools import islice

from utils.test_case import TestCase
from d20_input import INPUT

TEST_CASES = [
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
""", 273)
]

EXPECTED_IMAGE = """
.#.#..#.##...#.##..#####
###....#.#....#..#......
##.##.###.#.#..######...
###.#####...#.#####.#..#
##.#....#.##.####...#.##
...########.#....#####.#
....#..#...##..#.#.###..
.####...#..#.....#......
#..#.##..#..###.#.##....
#.####..#.####.#.#.###..
###.#.#...#.######.#..##
#.####....##..########.#
##..##.#...#...#.#.#.#..
...#..#..#.#.##..###.###
.#.#....#.##.#...###.##.
###.#...#..#.##.######..
.#.#.###.##.##.#..#.##..
.####.###.#...###.#..#.#
..#.#..#..#.#.#.####.###
#..####...#.#.#.###.###.
#####..#####...###....##
#.##..#..#...#..####...#
.#.###..##..##..####.##.
...###...##...#...#..###
"""

# 1951    2311    3079
# 2729    1427    2473
# 2971    1489    1171

# (1951, 2311, 3079, 2729, 1427, 2473, 2971, 1489, 1171)

MONSTER = [
    '                  # ',
    '#    ##    ##    ###',
    ' #  #  #  #  #  #   ',
]

EXPECTED_IMAGE_WITH_MONSTER = """
.####...#####..#...###..
#####..#..#.#.####..#.#.
.#.#...#.###...#.##.O#..
#.O.##.OO#.#.OO.##.OOO##
..#O.#O#.O##O..O.#O##.##
...#.#..##.##...#..#..##
#.##.#..#.#..#..##.#.#..
.###.##.....#...###.#...
#.####.#.#....##.#..#.#.
##...#..#....#..#...####
..#.##...###..#.#####..#
....#.##.#.#####....#...
..##.##.###.....#.##..#.
#...#...###..####....##.
.#.##...#.##.#.#.###...#
#.###.#..####...##..#...
#.###...#.##...#.##O###.
.O##.#OO.###OO##..OOO##.
..O#.O..O..O.#O##O##.###
#.#..##.########..#..##.
#.#####..#.#...##..#....
#....##..#.#########..##
#...#.....#..##...###.##
#..###....##.#...##.##.#
"""

Tile = namedtuple('Tile', 'id borders ops')


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
        (tile.borders[RIGHT], flipped_side(tile.borders[BOTTOM]), tile.borders[LEFT], flipped_side(tile.borders[TOP])),
        tile.ops + ('rotate',),
    )


assert rotate(Tile(1, (1, 2, 3, 4), ops=tuple())) == Tile(1, (2, 768, 4, 512), ops=('rotate',))


def flipx(tile):
    return Tile(
        tile.id,
        (flipped_side(tile.borders[TOP]), tile.borders[LEFT], flipped_side(tile.borders[BOTTOM]), tile.borders[RIGHT]),
        tile.ops + ('flipx',),
    )


assert flipx(Tile(1, (1, 2, 3, 4), ops=tuple())) == \
       Tile(1, (int('1000000000', 2), 4, int('1100000000', 2), 2), ops=('flipx',))


def flipy(tile):
    return Tile(
        tile.id,
        (tile.borders[BOTTOM], flipped_side(tile.borders[RIGHT]), tile.borders[TOP], flipped_side(tile.borders[LEFT])),
        tile.ops + ('flipy',),
    )


assert flipy(Tile(1, (1, 2, 3, 4), ops=tuple())) == \
       Tile(1, (3, int('0100000000', 2), 1, int('0010000000', 2)), ops=('flipy',))


def parse_tile(tile_src):
    tile_lines = [line.strip() for line in tile_src.strip().split('\n')]
    id = int(re.match(r'Tile (\d+):', tile_lines[0]).group(1))
    top_border = border_to_int(tile_lines[1])
    bottom_border = border_to_int(tile_lines[-1])
    left_border = border_to_int(''.join(tile_lines[i][0] for i in range(1, len(tile_lines))))
    right_border = border_to_int(''.join(tile_lines[i][-1] for i in range(1, len(tile_lines))))
    tile = Tile(id, (top_border, right_border, bottom_border, left_border), ops=tuple())
    assert all(len(tile_lines[i]) == 10 for i in range(1, len(tile_lines)))
    return id, tile


def pixels_flipx(rows):
    return [row[::-1] for row in rows]


assert pixels_flipx(['123', '456', '789']) == ['321', '654', '987']


def pixels_flipy(rows):
    return rows[::-1]


assert pixels_flipy(['123', '456', '789']) == ['789', '456', '123']


def pixels_rotate(rows):
    return [''.join(new_row) for new_row in zip(*pixels_flipx(rows))]


assert pixels_rotate(['123', '456', '789']) == ['369', '258', '147']


def parse_tile_pixels(tile_src, tiles):
    tile_lines = [line.strip() for line in tile_src.strip().split('\n')]
    id = int(re.match(r'Tile (\d+):', tile_lines[0]).group(1))
    rows = tile_lines[1:]
    rows = [row[1:-1] for row in rows[1:-1]]
    for op in tiles[id].ops:
        if op == 'rotate':
            rows = pixels_rotate(rows)
        elif op == 'flipx':
            rows = pixels_flipx(rows)
        elif op == 'flipy':
            rows = pixels_flipy(rows)
    return (id, rows)


def find_tile(tiles, side, matching_border):
    flipped_matching_border = flipped_side(matching_border)
    for next_tile in tiles:
        if matching_border not in next_tile.borders and flipped_matching_border not in next_tile.borders:
            continue
        for i in range(4):
            if next_tile.borders[side] == matching_border:
                return next_tile
            next_tile = rotate(next_tile)
        next_tile = flipx(next_tile)
        for i in range(4):
            if next_tile.borders[side] == matching_border:
                return next_tile
            next_tile = rotate(next_tile)
    return Tile(next_tile.id, (-1, -1, -1, -1), ops=tuple())
    # assert False, 'not found'


def replace_one_monster(pixels, i, j, monster, monster_height, monster_width):
    for k in range(0, monster_height):
        for l in range(0, monster_width):
            if monster[k][l] == '#':
                if pixels[i + k][j + l] != '#':
                    return 0

    # we found one, let's replace it
    print(f'found monster on {i}, {j}')
    for k in range(0, monster_height):
        for l in range(0, monster_width):
            if monster[k][l] == '#':
                pixels[i + k][j + l] = 'O'
    return 1


def replace_monster(pixels, monster):
    monster_height = len(monster)
    monster_width = len(monster[0])
    found_monsters = 0
    for i in range(0, len(pixels) - monster_height):
        for j in range(0, len(pixels[i]) - monster_width):
            found_monsters += replace_one_monster(pixels, i, j, monster, monster_height, monster_width)
    return found_monsters


def arrange_puzzle(tiles, first_corner, outer_borders, image_size):
    # as we know that all borders are unique, arranging the puzzle is just finding the next tile, and placing it
    # correctly

    # we start with any corner
    tiles.pop(first_corner.id)
    while first_corner.borders[TOP] not in outer_borders or first_corner.borders[LEFT] not in outer_borders:
        first_corner = rotate(first_corner)
    puzzle = [first_corner]  # rotate until outer borders are LEFT & TOP
    while tiles:
        if len(puzzle) % image_size == 0:  # beginning of row
            border_above = puzzle[-image_size].borders[BOTTOM]
            next_tile = find_tile(tiles.values(), TOP, border_above)
        else:  ## middle of row
            border_left = puzzle[-1].borders[RIGHT]
            next_tile = find_tile(tiles.values(), LEFT, border_left)
        puzzle.append(next_tile)
        tiles.pop(next_tile.id)

    return [puzzle[i:i + image_size] for i in range(0, len(puzzle), image_size)]


def solve(input):
    tiles = dict(parse_tile(tile_section) for tile_section in input.strip().split('\n\n'))
    image_size = math.isqrt(len(tiles))

    all_borders = (
            [border for tile in tiles.values() for border in tile.borders] +
            [flipped_side(border) for tile in tiles.values() for border in tile.borders]
    )

    # all borders are unique, and the outer borders appear only once
    assert len(all_borders) == 2 * (len(set(all_borders)) - image_size * 4)

    border_count = Counter(all_borders)

    outer_borders = [border for border, count in border_count.items() if count == 1]
    assert (len(outer_borders)) == 2 * image_size * 4  # because they may be flipped

    # one tile is a corner if it has 2 outer borders
    corners = [
        tile
        for tile in tiles.values()
        if 2 == len([border for border in tile.borders if border in outer_borders])
    ]

    try:
        first_corner = flipx([corner for corner in corners if corner.id == 1951][0])
    except IndexError:
        first_corner = corners[0]
    # first_corner = min(corners, key=lambda t: t.id)
    puzzle = arrange_puzzle(tiles, first_corner, outer_borders, image_size)
    for row in puzzle:
        print(''.join(f'|  {tile.borders[TOP]:^18}  |' for tile in row))
        print()
        print(''.join(f'|  {tile.borders[LEFT]:^5}  {tile.id:^4}  {tile.borders[RIGHT]:^5}  |' for tile in row))
        print()
        print(''.join(f'|  {tile.borders[BOTTOM]:^18}  |' for tile in row))
        print()
        print()

    print('-')

    transformed_tiles = {tile.id: tile for row in puzzle for tile in row}

    tiles_pixels = dict(
        parse_tile_pixels(tile_section, transformed_tiles) for tile_section in input.strip().split('\n\n'))

    pixels = []
    for tile_row in puzzle:
        for pixel_rows in zip(*(tiles_pixels[tile.id] for tile in tile_row)):
            pixels.append([pixel for row in pixel_rows for pixel in row])

    for pixels_row in pixels:
        print(''.join(pixels_row))

    if image_size == 3:
        with open('actual_image.txt', 'w') as f:
            for pixels_row in pixels:
                f.write(''.join(pixels_row) + '\n')

        assert EXPECTED_IMAGE.strip() == '\n'.join(''.join(pixels_row) for pixels_row in pixels)

    # print('-')
    #
    # for tile_row in puzzle:
    #     for tile in tile_row:
    #         print(f'tile: {tile.id}')
    #         for pixel_row in tiles_pixels[tile.id]:
    #             print(pixel_row)
    #         print()
    # pixels = pixels_flipx(pixels_rotate(pixels_rotate(pixels_rotate(pixels))))
    pixels = [list(row) for row in pixels]
    monsters = [MONSTER, pixels_rotate(MONSTER), pixels_rotate(pixels_rotate(MONSTER)), pixels_rotate(pixels_rotate(pixels_rotate(MONSTER)))]
    monsters += [pixels_flipx(monster) for monster in monsters]
    for monster in monsters:
        found_monsters = replace_monster(pixels, monster)
        if found_monsters:
            break

    if image_size == 3:
        with open('actual_image_with_monster.txt', 'w') as f:
            for pixels_row in pixels:
                f.write(''.join(pixels_row) + '\n')

        # assert EXPECTED_IMAGE_WITH_MONSTER.strip() == '\n'.join(''.join(pixels_row) for pixels_row in pixels)

    # return math.prod(corner.id for corner in corners)
    return ''.join(''.join(row) for row in pixels).count('#')


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
