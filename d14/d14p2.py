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
        for variant2 in gen_variants(addr[1:]):
            if addr[0] == 'X':
                yield '0' + variant2
                yield '1' + variant2
            else:
                yield addr[0] + variant2


def addresses(addr):
    return {int(variant, 2) for variant in gen_variants(addr)}


print(list(gen_variants('1')))
print(list(gen_variants('X')))
print(list(gen_variants('X1')))
print(list(gen_variants('1X')))
print(list(gen_variants('X11X0')))


def pad(s):
    return '0' * (36 - len(s)) + s


def remaining(addr, other_addr):
    assert addr != other_addr
    s1 = addresses(addr)
    s2 = addresses(other_addr)
    remaining = [pad(bin(o)[2:]) for o in set.difference(s2, s1)]
    new_addr = ''
    n = len(remaining)
    for bits in zip(*remaining):
        if bits.count('1') == n:
            new_addr += '1'
        elif bits.count('0') == n:
            new_addr += '0'
        else:
            new_addr += 'X'
    return pad(new_addr)


# remaining('111', 'XXX')
# remaining('0110010X0100XX10001X11X1X11110XX1X11', '0110010X0100XX10001X11X1X11110XX1X11')


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

    # 2065709786551 too low
    #  3858655567424 wrong
    # 3858655568118 too high
    return sum(mem.values())


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
