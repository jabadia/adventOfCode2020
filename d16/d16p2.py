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
    rules_section, my_ticket_section, nearby_tickets_section = input.strip().split('\n\n')
    rules = {}
    for rule in rules_section.strip().split('\n'):
        field_name, ranges = rule.split(': ')
        ranges = ranges.split(' or ')
        ranges = [(int(n0), int(n1)) for n0, n1 in [re.match('(\d+)-(\d+)', r).groups() for r in ranges]]
        rules[field_name] = ranges

    valid_tickets = []
    for ticket in nearby_tickets_section.strip().split('\n'):
        if ticket.startswith('nearby'):
            continue
        ticket = [int(field_value) for field_value in ticket.split(',')]
        if not is_ticket_valid(ticket, rules):
            continue
        valid_tickets.append(ticket)

    print(valid_tickets)

    field_count = len(valid_tickets[0])
    good_fields = defaultdict(set)
    for field_name, ranges in rules.items():
        for i in range(field_count):
            is_good = all(is_field_valid(ticket[i], ranges) for ticket in valid_tickets)
            if is_good:
                # good_fields[field_name].add(i)
                good_fields[i].add(field_name)
    good_fields = dict(good_fields)

    known_fields = {}
    while good_fields:
        for i, field_names in good_fields.items():
            if len(field_names) == 1:
                field_name = field_names.pop()
                known_fields[i] = field_name
                good_fields.pop(i)
                for other_field_names in good_fields.values():
                    other_field_names -= {field_name}
                break

    my_ticket = [int(n) for n in my_ticket_section.strip().split('\n')[1].split(',')]

    return math.prod(
        my_ticket[i]
        for i, name in known_fields.items()
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
