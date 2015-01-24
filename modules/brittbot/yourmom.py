#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/yourmom.py - Your mom jokes

import random

from modules.brittbot.filters import smart_ignore


@smart_ignore
def your_mom(jenni, msg):
    if jenni.nick in msg.lower():
        return
    msg = "Your mom %s %s." % (
        msg.groups()[0],
        msg.groups()[1],
    )
    if len(msg.split(" ")) > 20:
        return
    if random.choice(range(75)) == 0:
        jenni.say(msg)
your_mom.rule = r"^.* (is|has|used to be) (.+)\W?$"
your_mom.priority = 'medium'
