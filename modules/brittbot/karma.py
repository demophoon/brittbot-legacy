#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/karma.py - Fuck it, Ship it!

import re
import random

from modules.brittbot import (
    filters,
)


def setup_karma_brain(jenni):
    brain = jenni.brain
    if 'karma' not in brain:
        brain['karma'] = {}
        jenni.save_brain()

karma = "(?:"
karma += "([a-zA-Z0-9]+)(\+\+|--)|"
karma += "\((.+)\)(\+\+|--)|"
karma += "(\+\+|--)([a-zA-Z0-9]+)|"
karma += "(\+\+|--)\((.+)\)|"
karma += "\((inc|dec) (.+)\)"
karma += ")+"

positive_karma = ['++', 'inc']
negitive_karma = ['--', 'dec']

positive_sayings = [
    "has leveled up!",
    "1 up",
    "has collected $200!",
    "+1",
]
negitive_sayings = [
    "-1",
    "womp womp womp.",
    "lost a life.",
]


@filters.smart_ignore
def karma_award(jenni, msg):
    if not msg.owner and msg.sender == "#r/kansascity":
        return
    setup_karma_brain(jenni)
    karmas = re.findall(re.compile(karma), msg)
    print karmas
    for item in karmas:
        item = [x for x in item if x]
        for k in positive_karma:
            if k in item:
                awarded = 1
                item = [x for x in item if x not in positive_karma][0]
                break
        for k in negitive_karma:
            if k in item:
                awarded = -1
                item = [x for x in item if x not in negitive_karma][0]
                break
        if len(item) < 2:
            return
        if item not in jenni.brain['karma']:
            jenni.brain['karma'][item] = 0
        jenni.brain['karma'][item] += awarded
        if awarded >= 1:
            saying = random.choice(positive_sayings)
        else:
            saying = random.choice(negitive_sayings)
        jenni.say("%s %s (Karma: %s)" % (
            item, saying, jenni.brain['karma'][item]
        ))
        jenni.save_brain()
karma_award.rule = r".*" + karma
karma_award.priority = 'medium'
