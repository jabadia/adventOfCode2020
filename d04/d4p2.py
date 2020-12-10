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

REQUIRED_FIELDS = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
ALLOWED_FIELDS = REQUIRED_FIELDS.union({'cid'})


def validate_hgt(field_value):
    magnitude, units = re.match(r"(\d+)(in|cm)$", field_value).groups()
    return (units == 'cm' and 150 <= int(magnitude) <= 193) or (units == 'in' and 59 <= int(field_value[:-2]) <= 76)


VALIDATORS = {
    'byr': lambda field_value: 1920 <= int(field_value) <= 2002,
    'iyr': lambda field_value: 2010 <= int(field_value) <= 2020,
    'eyr': lambda field_value: 2020 <= int(field_value) <= 2030,
    'hgt': validate_hgt,
    'hcl': lambda field_value: re.match(r'#[0-9a-f]{6}$', field_value),
    'ecl': lambda field_value: field_value in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'),
    'pid': lambda field_value: re.match(r'\d{9}$', field_value),
    'cid': lambda field_value: True
}


def is_field_valid(field_name, field_value):
    try:
        return VALIDATORS[field_name](field_value)
    except (KeyError, ValueError, AttributeError):
        return False


assert is_field_valid('byr', '2002')
assert not is_field_valid('byr', '2003')
assert is_field_valid('hgt', '60in')
assert is_field_valid('hgt', '190cm')
assert not is_field_valid('hgt', '190in')
assert not is_field_valid('hgt', '190')
assert is_field_valid('hcl', '#123abc')
assert not is_field_valid('hcl', '#123abz')
assert not is_field_valid('hcl', '123abc')
assert is_field_valid('ecl', 'brn')
assert not is_field_valid('ecl', 'wat')
assert is_field_valid('pid', '000000001')
assert not is_field_valid('pid', '0123456789')


def is_valid(password):
    fields = dict(field.split(':') for field in password.replace('\n', ' ').split(' '))
    missing_fields = REQUIRED_FIELDS.difference(fields)
    unexpected_fields = set(fields).difference(ALLOWED_FIELDS)

    return not missing_fields and not unexpected_fields and all(
        is_field_valid(field_name, field_value) for field_name, field_value in fields.items()
    )


def solve(input):
    return sum(is_valid(password) for password in input.strip().split('\n\n'))


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    print(solve(INPUT))
