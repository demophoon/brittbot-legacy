#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/karma.py - Fuck it, Ship it!

import re
import random


def setup_karma_brain(jenni):
    brain = jenni.brain
    if 'karma' not in brain:
        brain['karma'] = {}
        jenni.brain.save()

karma = "(?:"
karma += "([a-zA-Z0-9\.]+)(\+\+|--)|"
karma += "\((.+)\)(\+\+|--)|"
karma += "(\+\+|--)([a-zA-Z0-9\.]+)|"
karma += "(\+\+|--)\((.+)\)|"
karma += "\((inc|dec) (.+)\)"
karma += ")+"

positive_karma = ['++', 'inc']
negitive_karma = ['--', 'dec']

positive_sayings = [
    "{0} has leveled up!",
    "{0} 1 up",
    "{0} has collected $200!",
    "{0} +1",
    "A winrar is {0}",
]
negitive_sayings = [
    "{0} -1",
    "{0} womp womp womp.",
    "{0} lost a life.",
]


def karma_award(jenni, msg):
    import time
    fixed_items = {
        'nokogiri': -666,
        'comcast': -666,
        'charter': -666,
        'c': -2147483648,
    }
    negitive_only = [
        "bash",
        'nokogiri',
        'ruby',
        'charter',
    ]
    decay = {
        "bash": {
            'rate': .001,
            'starting_time': 0,
        },
        "hipchat": {
            'rate': 1,
            'starting_time': 1434391283,
        },
        "nic": {
            'rate': .1,
            'starting_time': 1434148095,
        },
    }
    setup_karma_brain(jenni)
    karmas = re.findall(re.compile(karma), msg)
    karma_replies = []
    items_awarded = []
    for item in karmas:
        item = [x.lower() for x in item if x]
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
        if len(item) <= 2 and item.lower() != "c" and item not in jenni.online_users[msg.sender]:
            return
        if item.lower() == msg.nick.lower():
            return
        if item.lower() == jenni.nick.lower():
            return
            item = msg.nick.lower()
        if item.lower() in items_awarded:
            continue
        is_tricky = any([
            ("born" in item or "bourne" in item) and "again" in item,
            "shell" in item,
            "bash" in item,
            re.match(r"b+a+s+h+", item),
        ])
        if item.lower() in negitive_only or is_tricky:
            if is_tricky:
                item = 'bash'
            if awarded > 0:
                jenni.reply(random.choice([
                    "Do you want to be friends or not?",
                    "nou.",
                    "Stop that.",
                    "D:<",
                    "I cannot do that for you",
                    "Nice try.",
                    "I've fixed that for you",
                ]))
            awarded = -1

        if item not in jenni.brain['karma']:
            jenni.brain['karma'][item] = 0
        jenni.brain['karma'][item] += awarded
        items_awarded.append(item.lower())
        if awarded >= 1:
            saying = random.choice(positive_sayings)
        else:
            saying = random.choice(negitive_sayings)
        karma_points = jenni.brain['karma'][item]
        if item.lower() in fixed_items:
            karma_points = fixed_items[item.lower()]
        if item.lower() in decay:
            karma_points -= int((time.time() - decay[item]['starting_time']) / decay[item]['rate'])
        commentary = saying.format(item)
        karma_replies.append("{0} (Karma: {1})".format(
            commentary, "{:,}".format(karma_points)
        ))
    jenni.say(", ".join(karma_replies))
    jenni.brain.save()
karma_award.rule = r".*" + karma
karma_award.priority = 'medium'


def karma_query(jenni, msg):
    item = msg.groups()[0]
    if re.match(r"^!karma (.+)( -?\d+)", msg):
        item = re.match(r"^!karma (.+)( -?\d+)", msg).groups()[0]
        if not msg.admin:
            return
        value = int(re.match(r"^!karma (.+)( -?\d+)", msg).groups()[1])
        jenni.brain['karma'][item] = value
    if item in jenni.brain['karma']:
        jenni.say("%s has %s karma." % (
            item, jenni.brain['karma'][item]
        ))
karma_query.rule = r"^!karma (.+)( -?\d+)?"
