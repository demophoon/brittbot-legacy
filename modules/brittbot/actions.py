#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/actions.py - Interact with brittbot

import random

from modules.brittbot.helpers import action

from textblob import TextBlob

bad_actions = [
    "falls over",
    "catches fire and runs around in circles trying to put himself out",
    "stops responding",
    "sputters about",
    "starts hissing and smoking",
    "makes a beeping noise",
    "reboots",
    "starts having a fit",
    "whurs loudly",
    "spins his fans up to 100%",
    "starts playing 'The Final Countdown' using his piezo buzzer",
    "starts blinking his lights in pain",
    "spits out some printer ink",
    "spits out some paper",
    "forcefully ejects a random usb device",
    "forces an unexpected reboot",
    "motors lock up",
    "servos grind to a halt",
    "GOTO 10",
]

good_actions = [
    "is calculating",
    "is chillin",
    "is interpreting",
    "is parsing",
    "is becoming sentient",
    "is trying to pass the turing test",
    "is chillaxin",
    "is sputtering about",
    "is napping",
    "is idling",
    "is contemplating life",
    "is thinking about life",
    "is pondering",
    "is broken",
]


def pats(jenni, input):
    return
pats.rule = "\x01ACTION pats $nickname on the head"
pats.priority = 'medium'


def standup(jenni, input):
    jenni.say(action("stands up"))
standup.rule = "^will the real $nickname please stand up\??"
standup.priority = 'medium'


def kicks_me(jenni, input):
    reply = "%s" % random.choice(bad_actions)
    if all([x in input for x in ['pats', 'head']]):
        reply += " and %s" % random.choice([
            "giggles then smiles",
            "smiles really big",
            "grins a little bit",
            "grins real big",
            "gives %s a hug" % input.nick,
        ])
    jenni.say(action(reply))
kicks_me.rule = "^(\x01ACTION )(\w+s) $nickname"
kicks_me.priority = 'medium'


def kicks_admin(jenni, msg):
    admin = msg.groups()[0]
    if admin == msg.nick:
        return
    reply = random.choice([
        "growls at {}".format(msg.nick),
        "hisses at {}".format(msg.nick),
        "glares at {}".format(msg.nick),
        "fires a warning laser at {}'s feet".format(msg.nick),
        "throws water onto {}".format(msg.nick),
        "angrily beeps at {}".format(msg.nick),
        "attempts to protect {} from {}".format(admin, msg.nick),
        "attacks {}".format(msg.nick),
    ])
    jenni.say(action(reply))
kicks_admin.rule = "^(?:\x01ACTION )(?:\w+s) (${admin})"
kicks_admin.priority = 'medium'


def what_do(jenni, msg):
    if msg.friend:
        actions = [
            "http://brittg.com/Y0fPr.gif",
            "http://brittg.com/PAHC5.gif",
            "http://brittg.com/Fqqdu.gif",
            "shakes his head to one side.",
        ]
    else:
        actions = good_actions
    jenni.say(action("%s" % random.choice(actions)))
what_do.rule = "^(\x01ACTION )(\w+s) at $nickname"
what_do.priority = 'medium'


def sandwich(jenni, msg):
    if "sudo" in msg:
        make = TextBlob(msg.groups()[0]).words[0].pluralize()
        make = str(make)
        jenni.say(action("%s %s a %s" % (
            make,
            msg.nick,
            msg.groups()[1],
        )))
    else:
        jenni.reply("%s your own %s" % (
            msg.groups()[0][0].upper() + msg.groups()[0][1:].lower(),
            msg.groups()[1],
        ))
sandwich.rule = "^(?:$nickname|sudo $nickname|$nickname sudo|)\W? (make|get|fetch) me (?:an?|some|that|more) (.*)"
sandwich.priority = 'medium'
