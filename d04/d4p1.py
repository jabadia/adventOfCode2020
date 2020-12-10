from utils.test_case import TestCase
from d4_input import INPUT

TEST_CASES = [
    TestCase("""
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
""", 2)
]

REQUIRED_FIELDS = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'}


def is_valid(password):
    fields = set(field.split(':')[0] for field in password.replace('\n', ' ').split(' '))
    missing_fields = REQUIRED_FIELDS.difference(fields)
    return len(missing_fields) == 0 or len(missing_fields) == 1 and 'cid' in missing_fields


def solve(input):
    return sum(is_valid(password) for password in input.strip().split('\n\n'))


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    print(solve(INPUT))
