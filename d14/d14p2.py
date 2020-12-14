import re
import time
from collections import Counter

from utils.test_case import TestCase
from d14_input import INPUT

TEST_CASES = [
    TestCase("""
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
""", 208),
]


def gen_variants(addr):
    if not addr:
        yield ''
    else:
        for rest in gen_variants(addr[1:]):
            if addr[0] == 'X':
                yield '0' + rest
                yield '1' + rest
            else:
                yield addr[0] + rest


def addresses(addr):
    return {int(variant, 2) for variant in gen_variants(addr)}


assert list(gen_variants('1')) == ['1']
assert list(gen_variants('X')) == ['0', '1']
assert list(gen_variants('X1')) == ['01', '11']
assert list(gen_variants('1X')) == ['10', '11']
assert list(gen_variants('X11X0')) == ['01100', '11100', '01110', '11110']


def pad(s):
    return '0' * (36 - len(s)) + s


def solve(input):
    n = len(input.strip().split('\n'))
    mem = {}
    for i, line in enumerate(input.strip().split('\n')):
        print(i, n)
        if line.startswith('mask'):
            mask = line.split(' = ')[1].strip()
        else:
            addr, value = [int(part) for part in re.match('mem\[(\d+)] = (\d+)$', line).groups()]
            bin_addr = pad(bin(addr)[2:])
            masked_addr = ''.join(bit if maskbit == '0' else maskbit for bit, maskbit in zip(bin_addr, mask))

            for one_addr in addresses(masked_addr):
                mem[one_addr] = value

    return sum(mem.values())


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
