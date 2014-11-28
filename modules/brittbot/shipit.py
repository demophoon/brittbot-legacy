#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/shipit.py - Fuck it, Ship it!

import random

from modules.brittbot import (
    filters,
)


@filters.smart_ignore
def ship_it(jenni, input):
    ship_its = [
        "FUCK IT. SHIP IT.",
        "FUCK IT. LETS SHIP IT.",
        "SHIP IT NOW.",
        "SHIP IT.",
    ]
    msg = random.choice(ship_its)
    jenni.msg(input.sender, msg)
ship_it.rule = r".*\bship it\b.*"
ship_it.priority = 'medium'
