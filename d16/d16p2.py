import math
import re
import time
from collections import defaultdict

from utils.test_case import TestCase
from d16_input import INPUT

TEST_CASES = [
    TestCase("""
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
    """, ['row', 'class', 'seat'])
]


def is_field_valid(field_value, ranges):
    return any(range_min <= field_value <= range_max for range_min, range_max in ranges)


def is_ticket_valid(ticket, rules):
    return all(
        any(is_field_valid(field_value, ranges) for ranges in rules.values())
        for field_value in ticket
    )


def solve(input):

    # separate input into 3 sections
    rules_section, my_ticket_section, nearby_tickets_section = input.strip().split('\n\n')

    # parse rules
    rules = {}
    for rule in rules_section.strip().split('\n'):
        field_name, ranges = rule.split(': ')
        rules[field_name] = [
            (int(n0), int(n1))
            for n0, n1 in [
                re.match('(\d+)-(\d+)', r).groups()
                for r in ranges.split(' or ')
            ]
        ]

    # find valid tickets
    valid_tickets = [
        ticket
        for ticket in
        [
            [int(field_value) for field_value in ticket_line.split(',')]
            for ticket_line in nearby_tickets_section.strip().split('\n')
            if not ticket_line.startswith('nearby')
        ]
        if is_ticket_valid(ticket, rules)
    ]

    # find what columns can be which fields
    columns = zip(*valid_tickets)  # transpose tickets into columns

    possible_fields = {
        col_index: set(
            field_name
            for field_name, ranges in rules.items()
            if all(is_field_valid(value, ranges) for value in column)
        )
        for col_index, column in enumerate(columns)
    }
    # possible_fields = dict { key = col_index, value = set(field names) }

    # resolve multiple possibilities by elimination
    solved_fields = {}
    while possible_fields:
        col_index, field_names = min(possible_fields.items(), key=lambda pair: len(pair[1]))
        assert len(field_names) == 1
        field_name = field_names.pop()
        solved_fields[col_index] = field_name
        possible_fields.pop(col_index)
        for other_field_names in possible_fields.values():
            other_field_names -= {field_name}

    # parse my ticket
    my_ticket = [int(n) for n in my_ticket_section.strip().split('\n')[1].split(',')]

    # return solution
    return math.prod(
        my_ticket[col_index]
        for col_index, name in solved_fields.items()
        if name.startswith('departure')
    )


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
