#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/actions.py - Interact with brittbot

import random

from modules.brittbot.filters import smart_ignore
from modules.brittbot.helpers import action


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
    "fans spin up to 100%",
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
    "calculating",
    "chillin",
    "interpreting",
    "parsing",
    "becoming sentient",
    "trying to pass the turing test",
    "chillaxin",
    "hanging",
    "sputtering about",
    "napping",
    "idling",
    "contemplating life",
    "thinking about life",
    "pondering",
    "broken",
]


@smart_ignore
def pats(jenni, input):
    jenni.say(action(random.choice([
        "giggles and smiles",
        "smiles really big",
        "grins a little bit",
        "grins real big",
        "gives %s a hug" % input.nick,
    ])))
pats.rule = "\x01ACTION pats $nickname on the head"
pats.priority = 'medium'


@smart_ignore
def standup(jenni, input):
    jenni.say(action("stands up"))
standup.rule = "^will the real $nickname please stand up\??"
standup.priority = 'medium'


@smart_ignore
def kicks_me(jenni, input):
    jenni.say(action("%s" % random.choice(bad_actions)))
kicks_me.rule = "^(\x01ACTION )(\w+s) $nickname"
kicks_me.priority = 'medium'


@smart_ignore
def what_do(jenni, input):
    jenni.say(action("is %s" % random.choice(good_actions)))
what_do.rule = "^(\x01ACTION )(\w+s) at $nickname"
what_do.priority = 'medium'


@smart_ignore
def sandwich(jenni, input):
    if "sudo" in input:
        jenni.say(action("makes %s a sandwich" % input.nick))
    else:
        jenni.say("Make your own sandwich")
sandwich.rule = "^($nickname|sudo $nickname)\W? make me a (sandwich|sammich)"
sandwich.priority = 'medium'
