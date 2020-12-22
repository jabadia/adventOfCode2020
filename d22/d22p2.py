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
""", 291),
    TestCase("""
Player 1:
43
19

Player 2:
2
29
14
""", None)
]


def recursive_combat(player1_cards, player2_cards):
    seen_games = set()

    while player1_cards and player2_cards:
        round = tuple(player1_cards) + tuple(player2_cards)
        if round in seen_games:
            return True  # player 1 wins
        seen_games.add(round)

        p1_card = player1_cards.popleft()
        p2_card = player2_cards.popleft()

        p1_won = None
        if len(player1_cards) >= p1_card and len(player2_cards) >= p2_card:
            p1_won = recursive_combat(deque(player1_cards), deque(player2_cards))

        if p1_won or p1_won is None and p1_card > p2_card:
            player1_cards.extend([p1_card, p2_card])
        else:
            assert p1_won is False or p1_won is None and p2_card > p1_card
            player2_cards.extend([p2_card, p1_card])

    return len(player1_cards) > len(player2_cards)


def solve(input):
    players = [None]
    for player_cards in input.strip().split('\n\n'):
        cards = deque(int(card) for card in player_cards.strip().split('\n')[1:])
        players.append(cards)

    p1_won = recursive_combat(players[1], players[2])

    return sum([(i + 1) * card for i, card in enumerate(reversed(players[1] or players[2]))])


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
