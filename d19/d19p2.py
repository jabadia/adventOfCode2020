import regex
import time

from utils.test_case import TestCase
from d19_input import INPUT

TEST_CASES = [
    TestCase("""
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
""", 12),
]


def generate_values(rules, start):
    for part in rules[start].split(' | '):
        if part in 'ab':
            yield part
        else:
            children = part.split()
            if len(children) == 1:
                for value in generate_values(rules, int(children[0])):
                    yield value
            elif len(children) == 2:
                for v1 in generate_values(rules, int(children[0])):
                    for v2 in generate_values(rules, int(children[1])):
                        yield v1 + v2
            else:
                assert False, 'unexpected'


def solve(input):
    rules_section, messages = input.strip().split('\n\n')

    new_rules = [
        '8: 42 | 42 8',
        '11: 42 31 | 42 11 31',
    ]

    rules = {}
    for rule_line in rules_section.split('\n') + new_rules:
        id, rule = rule_line.strip().split(': ')
        rules[int(id)] = rule.replace('"', '')

    # relevant rules are:
    # 0: 8 11
    # 8: 42 | 42 8
    # 11: 42 31 | 42 11 31

    # rule 8 means: one or more repetitions of 42
    # rule 11 means: n repetitions of 42 followed by n (same number) repetitions of 31, with n >= 1
    #
    # therefore rule 0 can be restated to
    # n repetitions of rule 42 followed by m repetitions of rule 31
    # with n > m

    regex_42 = '|'.join(set(generate_values(rules, 42)))
    regex_31 = '|'.join(set(generate_values(rules, 31)))

    full_regex = f'({regex_42})+({regex_31})+'

    def is_valid(message, full_regex):
        # I had to use https://pypi.org/project/regex/, because I couldn't find how to get the number of
        # repetitions captured in each group with builit-in re, :-(
        matches = regex.fullmatch(full_regex, message)
        return matches and len(matches.captures(1)) > len(matches.captures(2))

    return sum(1 for message in messages.strip().split('\n') if is_valid(message, full_regex))


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
