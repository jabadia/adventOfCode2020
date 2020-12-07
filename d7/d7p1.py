import re
from collections import defaultdict

from utils.test_case import TestCase
from d7_input import INPUT

TEST_CASES = [
    TestCase("""
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
""", 4),
]


def get_valid_colors_for(color, is_contained):
    colors = is_contained.get(color, [])
    valid_colors = set(colors)
    for other_color in colors:
        valid_colors.update(get_valid_colors_for(other_color, is_contained))
    return valid_colors


def solve(input):
    is_contained = defaultdict(list)
    for rule in input.strip().split('\n'):
        outer, inner = rule.split(' bags contain ')
        inner = [inner_part.split(' ')[:3] for inner_part in inner.split(', ')]
        for inner_rule in inner:
            count, color = inner_rule[0], ' '.join(inner_rule[1:])
            is_contained[color].append(outer)
    is_contained = dict(is_contained)

    return len(get_valid_colors_for('shiny gold', is_contained))


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    print(solve(INPUT))
