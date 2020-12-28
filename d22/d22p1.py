import re
import time
from collections import deque

from utils.test_case import TestCase
from d22_input import INPUT

TEST_CASES = [
    TestCase("""
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
""", 306),
]


def solve(input):
    players = [None]
    for player_cards in input.strip().split('\n\n'):
        cards = deque(int(card) for card in player_cards.strip().split('\n')[1:])
        players.append(cards)

    while players[1] and players[2]:
        p1_card = players[1].popleft()
        p2_card = players[2].popleft()
        if p1_card > p2_card:
            players[1].extend([p1_card, p2_card])
        else:
            players[2].extend([p2_card, p1_card])

    return sum((i+1) * card for i, card in enumerate(reversed(players[1] or players[2])))


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
