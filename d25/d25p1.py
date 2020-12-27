import time

from utils.test_case import TestCase
from d25_input import INPUT

TEST_CASES = [
    TestCase("""
5764801
17807724
""", (8, 11, 14897079)),
]


def find_loop(key, subject):
    value = 1
    loop_size = 0
    while value != key:
        value = value * subject
        value %= 20201227
        loop_size += 1
    return loop_size


def apply_loop(loop_size, subject):
    value = 1
    for i in range(loop_size):
        value = value * subject
        value %= 20201227
    return value


def solve(input):
    card_key, door_key = [int(key) for key in input.strip().split('\n')]
    card_loop_size = find_loop(card_key, 7)
    door_loop_size = find_loop(door_key, 7)
    return card_loop_size, door_loop_size, apply_loop(card_loop_size, door_key)


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
