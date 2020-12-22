import re
import time
from collections import deque
from itertools import islice

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
    #     TestCase("""
    # Player 1:
    # 43
    # 19
    #
    # Player 2:
    # 2
    # 29
    # 14
    # """, None)
]

i = 0
def next_game_index():
    global i
    i += 1
    return i


def recursive_combat(player1_cards, player2_cards, out):
    seen_games = set()

    game_index = next_game_index()
    print(f'=== Game {game_index} ===', file=out)
    turn = 1

    while player1_cards and player2_cards:
        print(f'\n-- Round {turn} (Game {game_index}) --', file=out)
        round = (tuple(player1_cards), tuple(player2_cards))
        if round in seen_games:
            return True  # player 1 wins
        seen_games.add(round)

        print(f"Player 1's deck: {', '.join(str(card) for card in player1_cards)}", file=out)
        print(f"Player 2's deck: {', '.join(str(card) for card in player2_cards)}", file=out)

        p1_card = player1_cards.popleft()
        p2_card = player2_cards.popleft()

        print(f'Player 1 plays: {p1_card}', file=out)
        print(f'Player 2 plays: {p2_card}', file=out)

        p1_won = None
        if len(player1_cards) >= p1_card and len(player2_cards) >= p2_card:
            print('Playing a sub-game to determine the winner...\n', file=out)
            p1_won = recursive_combat(
                deque(islice(player1_cards, 0, p1_card)),
                deque(islice(player2_cards, 0, p2_card)),
                out
            )
            print(f'\n...anyway, back to game {game_index}.', file=out)

        if p1_won or p1_won is None and p1_card > p2_card:
            print(f'Player 1 wins round {turn} of game {game_index}!', file=out)
            player1_cards.extend([p1_card, p2_card])
        else:
            assert p1_won is False or p1_won is None and p2_card > p1_card
            print(f'Player 2 wins round {turn} of game {game_index}!', file=out)
            player2_cards.extend([p2_card, p1_card])

        turn += 1

    p1_won = len(player1_cards) > len(player2_cards)
    print(f'The winner of game {game_index} is player {1 if p1_won else 2}!', file=out)
    return p1_won


def solve(input):
    global i

    players = [None]
    for player_cards in input.strip().split('\n\n'):
        cards = deque(int(card) for card in player_cards.strip().split('\n')[1:])
        players.append(cards)

    i = 0
    with open('actual_gameplay.txt', 'w') as out:
        p1_won = recursive_combat(players[1], players[2], out)

        print(f"== Post-game results ==", file=out)
        print(f"Player 1's deck: {', '.join(str(card) for card in players[1])}", file=out)
        print(f"Player 2's deck: {', '.join(str(card) for card in players[2])}", file=out)

    return sum([(i + 1) * card for i, card in enumerate(reversed(players[1] or players[2]))])


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")

    # 32360  too low

    out.flush()
    out.close()
