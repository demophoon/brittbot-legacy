#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/dm.py - Attack monsters

from modules.brittbot.filters import smart_ignore


@smart_ignore
def attack_monster(jenni, msg):
    pass
attack_monster.rule = r"!attack (.*)"
attack_monster.priority = 'medium'
