import re
import time
from collections import defaultdict, Counter

from utils.test_case import TestCase
from d21_input import INPUT

TEST_CASES = [
    TestCase("""
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
""", 'mxmxvkd,sqjhc,fvjkl'),
]


def solve(input):
    possible_ingredients = {}
    foods = []
    for food in input.strip().split('\n'):
        ingredients, allergens = re.fullmatch('(.*) \(contains (.*)\)', food).groups()
        ingredients = ingredients.split()
        allergens = allergens.split(', ')
        foods.append(set(ingredients))
        for allergen in allergens:
            if allergen not in possible_ingredients:
                possible_ingredients[allergen] = set(ingredients)
            else:
                possible_ingredients[allergen] &= set(ingredients)

    # resolve multiple possibilities by elimination
    solved_ingredients = {}
    while possible_ingredients:
        allergen, ingredients = min(possible_ingredients.items(), key=lambda pair: len(pair[1]))
        assert len(ingredients) == 1
        ingredient = ingredients.pop()
        solved_ingredients[ingredient] = allergen
        possible_ingredients.pop(allergen)
        for other_ingredients in possible_ingredients.values():
            other_ingredients -= {ingredient}

    return ','.join(
        ingredient
        for allergen, ingredient in (
            sorted(
                (allergen, ingredient)
                for ingredient, allergen in solved_ingredients.items()
                if ingredient in solved_ingredients
            )
        )
    )


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    t0 = time.time()
    print(solve(INPUT))
    t1 = time.time()
    print(f"{(t1 - t0) * 1000:0.1f} ms")
