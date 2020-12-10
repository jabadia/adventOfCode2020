import os
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
""", 32),
    TestCase("""
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
""", 126)
]


def write_graph(contains):
    graph_path = 'dependencies.gv'
    output_path = graph_path.replace('.gv', '.pdf')
    with open(graph_path, 'w') as graph:
        graph.write('digraph G {\n')
        graph.write('rankdir=LR;\n')
        graph.write('node [shape=box];\n')
        for outer_bag, inner_bags in contains.items():
            for (count, inner_bag) in inner_bags:
                graph.write(f'\t"{outer_bag}" -> "{inner_bag}" [label={count}];\n')
        graph.write('}\n')
    cmd = f'dot -Tpdf {graph_path} -o {output_path}'
    os.system(cmd)
    print(f'converted to {output_path}')
    os.system(f'open {output_path}')


def get_total_bags(color, contains):
    return 1 + sum(
        get_total_bags(inner_color, contains) * inner_count
        for inner_count, inner_color in contains.get(color, [])
    )


def solve(input):
    contains = defaultdict(list)
    for rule in input.strip().split('\n'):
        outer, inner = rule.split(' bags contain ')
        inner = [inner_part.split(' ')[:3] for inner_part in inner.split(', ')]
        for inner_rule in inner:
            if inner_rule[0] != 'no':
                count, color = int(inner_rule[0]), ' '.join(inner_rule[1:])
                contains[outer].append((count, color))
    contains = dict(contains)

    write_graph(contains)

    return get_total_bags('shiny gold', contains) - 1


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    print(solve(INPUT))
