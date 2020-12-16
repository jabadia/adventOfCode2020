import re
import time

from utils.test_case import TestCase
from d16_input import INPUT

TEST_CASES = [
    TestCase("""
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
""", 71),
]


def is_field_valid(field_value, ranges):
    return any(
        range_min <= field_value <= range_max
        for range_min, range_max in ranges
    )


def solve(input):
    rules_section, my_ticket_section, nearby_tickets_section = input.strip().split('\n\n')
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

    error_rate = sum(
        sum(
            field_value
            for field_value in [int(v) for v in ticket.split(',')]
            if not any(is_field_valid(field_value, ranges) for ranges in rules.values())
        )
        for ticket in nearby_tickets_section.strip().split('\n')
        if not ticket.startswith('nearby')
    )
    return error_rate


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
