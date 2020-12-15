import time

from utils.test_case import TestCase
from d15_input import INPUT

TEST_CASES = [
    TestCase("0,3,6", 175594),
    # TestCase("1,3,2", 1),
    # TestCase("2,1,3", 10),
    # TestCase("1,2,3", 27),
    # TestCase("2,3,1", 78),
    # TestCase("3,2,1", 438),
    # TestCase("3,1,2", 1836),
]


def solve(input):
    starting_numbers = [int(n) for n in input.strip().split(',')]
    spoken = {number: i+1 for i, number in enumerate(starting_numbers[:-1])}
    last_spoken = starting_numbers[-1]

    for turn in range(len(starting_numbers), 30000000):
        if last_spoken in spoken:
            next = turn - spoken[last_spoken]
        else:
            next = 0

        spoken[last_spoken] = turn
        # print(f'turn {turn}: spoken: {last_spoken}')
        last_spoken = next

    return last_spoken


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
