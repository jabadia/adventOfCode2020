import re
from utils.test_case import TestCase
from d4_input import INPUT

TEST_CASES = [
    TestCase("""
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
""", 0),
    TestCase("""
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022
""", 3),
]

REQUIRED_FIELDS = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'}


def check_field(field_name, field_value):
    try:
        if field_name == 'byr':
            if not 1920 <= int(field_value) <= 2002:
                return False
        elif field_name == 'iyr':
            if not 2010 <= int(field_value) <= 2020:
                return False
        elif field_name == 'eyr':
            if not 2020 <= int(field_value) <= 2030:
                return False
        elif field_name == 'hgt':
            if field_value[-2:] == 'cm':
                if not 150 <= int(field_value[:-2]) <= 193:
                    return False
            elif field_value[-2:] == 'in':
                if not 59 <= int(field_value[:-2]) <= 76:
                    return False
            else:
                return False
        elif field_name == 'hcl':
            if not re.match(r'#[0-9a-f]{6}', field_value):
                return False
        elif field_name == 'ecl':
            if not field_value in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'):
                return False
        elif field_name == 'pid':
            if not re.match(r'\d{9}$', field_value):
                return False
        elif field_name == 'cid':
            pass
    except ValueError:
        return False

    return True


assert check_field('byr', '2002')
assert not check_field('byr', '2003')
assert check_field('hgt', '60in')
assert check_field('hgt', '190cm')
assert not check_field('hgt', '190in')
assert not check_field('hgt', '190')
assert check_field('hcl', '#123abc')
assert not check_field('hcl', '#123abz')
assert not check_field('hcl', '123abc')
assert check_field('ecl', 'brn')
assert not check_field('ecl', 'wat')
assert check_field('pid', '000000001')
assert not check_field('pid', '0123456789')


def is_valid(password):
    fields = dict(field.split(':') for field in password.replace('\n', ' ').split(' '))
    missing_fields = REQUIRED_FIELDS.difference(fields)
    if not (len(missing_fields) == 0 or len(missing_fields) == 1 and 'cid' in missing_fields):
        return False

    for field_name, field_value in fields.items():
        is_valid = check_field(field_name, field_value)
        if not is_valid:
            return False
    return True


def solve(input):
    return sum(is_valid(password) for password in input.strip().replace('\n\n', '|').split('|'))


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    print(solve(INPUT))
