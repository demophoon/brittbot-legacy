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
    return
pats.rule = "\x01ACTION pats $nickname on the head"
pats.priority = 'medium'


@smart_ignore
def standup(jenni, input):
    jenni.say(action("stands up"))
standup.rule = "^will the real $nickname please stand up\??"
standup.priority = 'medium'


@smart_ignore
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


@smart_ignore
def what_do(jenni, input):
    jenni.say(action("is %s" % random.choice(good_actions)))
what_do.rule = "^(\x01ACTION )(\w+s) at $nickname"
what_do.priority = 'medium'


@smart_ignore
def sandwich(jenni, msg):
    if "sudo" in msg:
        jenni.say(action("makes %s a %s" % (
            msg.nick,
            msg.groups()[0],
        )))
    else:
        jenni.reply("Make your own %s" % msg.groups()[0])
sandwich.rule = "^(?:$nickname|sudo $nickname|$nickname sudo|)\W? make me a (\w+)"
sandwich.priority = 'medium'
