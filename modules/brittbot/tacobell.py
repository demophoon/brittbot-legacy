#!/usr/bin/env python
# encoding: utf-8

import random

counts = [
    'Double',
    'Triple',
    'Quadruple',
]
adjectives = [
    'Beefy',
    'Cheesy',
    'Spicy',
    'Fiery',
    'Crunchy',
    'Crispy',
    'Loaded',
    'Grilled',
]
fillers = [
    'Potato',
    'Nacho Cheese',
    'Bean',
    'Black Bean',
    'Rice',
    'Ground Beef',
    'Shredded Chicken',
    'Chicken',
    'Steak',
    'Fajitas',
    u'Fritos®',
    u'Doritos® Locos',
]
meal_modifiers = [
    'Fiesta',
    'Fresco',
    'Fresco Grilled',
]
meals = [
    'Taco',
    'Soft Taco',
    u'Double Decker® Taco',
    'Taco Salad',
    'Burrito',
    'Gordita',
    'Chalupa',
    'Crunchwrap',
    'Quesadilla',
    'Griller',
    'Mexican Pizza',
    'Quesarito',
    'Crunchwrap Slider',
    'Tostada',
    u'Meximelt®',
    'XXL Grilled Stuft Burrito',
    'Smothered Burrito',
    'Combo Burrito',
    '5-Layer Burrito',
    '7-Layer Burrito',
    'Nachos',
    u'Nachos Bellgrande®',
    u'Doritos® Locos Taco',
    u'Doritos® Locos Gordita',
    u'Doritos® Locos Chalupa',
    u'Doritos® Locos Nachos',
]
modifiers = [
    'Crunch',
    u'Supreme®',
]

meats = [
    'Nacho Cheese',
    'Quesarito',
    'Quesadilla',
    'Griller',
    'Mexican Pizza',
    'Beef'
    'Beefy'
    'Ground Beef',
    'Shredded Chicken',
    'Chicken',
    'Steak',
    'Fajitas',
]

def get_next_phrase(phrases, skips=None, randomness=0.5, vegan=False):
    trues = int(randomness * 100)
    falses = int(100 - trues)
    chance = [True] * trues + [False] * falses
    if not random.choice(chance):
        return []
    if not skips:
        skips = []
    for _ in range(len(phrases)):
        word = random.choice(phrases)
        skip = False
        for s in skips:
            if s in word:
                skip = True
            if vegan:
                if s in meats:
                    skip = True
        if not skip:
            break
    return [word]


def generate_taco_bell(vegan=False):
    food = get_next_phrase(counts, randomness=.1, vegan=vegan)
    food += get_next_phrase(adjectives, skips=food, randomness=.85, vegan=vegan)
    food += get_next_phrase(fillers, skips=food, randomness=.75, vegan=vegan)
    food += get_next_phrase(meal_modifiers, skips=food, randomness=.1, vegan=vegan)
    food += get_next_phrase(meals, skips=food, randomness=1.0, vegan=vegan)
    food += get_next_phrase(modifiers, skips=food, randomness=.25, vegan=vegan)

    taco_modifiers = [
    ]
    return ' '.join(food)
