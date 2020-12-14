import re
import time

from utils.test_case import TestCase
from d14_input import INPUT

TEST_CASES = [
    TestCase("""
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
""", 165),
]


def solve(input):
    ones_mask = 0
    zeros_mask = 0
    mem = {}
    for line in input.strip().split('\n'):
        if line.startswith('mask'):
            mask = line.split(' = ')[1].strip()
            ones_mask = int(mask.replace('X', '0'), 2)
            zeros_mask = int(mask.replace('X', '1'), 2)
        else:
            addr, value = [int(part) for part in re.match('mem\[(\d+)] = (\d+)$', line).groups()]
            mem[addr] = value & zeros_mask | ones_mask

    return sum(mem.values())


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
