#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/adarkroom.py - A Dark Room in IRC

import time
import math
from modules.brittbot.helpers import notice


def init_adr_brain(jenni):
    brain = jenni.brain
    adr_version = "1.0.2"
    if 'adr' not in brain or brain['adr']['version'] != adr_version:
        now = int(time.time())
        brain['adr'] = {
            'version': adr_version,
            'events': {
                'fire': {
                    'last_update': now,
                    'value': 0,
                },
                'room': {
                    'last_update': now,
                    'value': 0,
                },
            },
            'inventory': {
                'wood': [0 for _ in range(8)],
            },
            'cooldown': {
                'stoke': 10,
                'wood': 15,
                'fire': 600,
                'room': 1800,
            },
        }
        jenni.brain.save()


def adr_modify_cooldown(jenni, msg):
    chan, item, duration, message = msg.groups()
    if jenni.brain['adr']['cooldown'].get(item):
        jenni.brain['adr']['cooldown'][item] = int(duration)
        if message:
            jenni.write(['NOTICE', chan, ":{}".format(message)])
adr_modify_cooldown.rule = r"^!adraward (#*\w+) (\w+) (\d+) (.*)"


def adr_light_fire(jenni, msg):
    init_adr_brain(jenni)
    brain = jenni.brain['adr']
    now = int(time.time())
    if len(brain['inventory']['wood']) > 5:
        brain['inventory']['wood'] = brain['inventory']['wood'][5:]
        brain['events']['fire']['value'] += 2
        brain['events']['fire']['last_update'] = now
        brain['events']['room']['value'] += 2
        brain['events']['room']['last_update'] = now
        notice(jenni, msg.sender, "The light from the fire spills from the windows, out into the dark.")
    else:
        notice(jenni, msg.sender, "Not enough wood to start the fire.")
        return
adr_light_fire.rule = r"^(\x01ACTION )lights (?:the )?fire"


def adr_stoke_fire(jenni, msg):
    init_adr_brain(jenni)
    now = int(time.time())
    brain = jenni.brain['adr']

    if brain['events']['fire']['value'] == 0:
        notice(jenni, msg.sender, "You need to light the fire first.")
        return

    last_update = brain['events']['fire']['last_update']
    if now - last_update < brain['cooldown']['stoke']:
        notice(jenni, msg.sender, "You must wait before stoking the fire again.")
        return

    duration = brain['cooldown']['fire']
    elapsed = now - brain['events']['fire']['last_update']
    dv = math.floor(float(elapsed) / float(duration))
    brain['events']['fire']['value'] -= dv
    brain['events']['fire']['value'] = max(0, brain['events']['fire']['value'])

    if len(brain['inventory']['wood']) > 0:
        brain['inventory']['wood'] = brain['inventory']['wood'][1:]
        brain['events']['fire']['value'] += 1
        brain['events']['fire']['last_update'] = now
        brain['events']['room']['value'] += 1
        brain['events']['room']['last_update'] = now
    else:
        notice(jenni, msg.sender, "Not enough wood to keep the fire going")
        return

    fire = None
    if brain['events']['fire']['value'] >= 4:
        brain['events']['fire']['value'] = 4
        fire = "roaring"
    elif brain['events']['fire']['value'] == 3:
        fire = "burning"
    elif brain['events']['fire']['value'] == 2:
        fire = "flickering"
    elif brain['events']['fire']['value'] == 1:
        fire = "smoldering"
    else:
        fire = "dead"

    duration = brain['cooldown']['room']
    elapsed = now - brain['events']['room']['last_update']
    dv = math.floor(float(elapsed) / float(duration))
    brain['events']['room']['value'] -= dv
    brain['events']['room']['value'] = max(0, brain['events']['room']['value'])
    room = None
    if brain['events']['room']['value'] >= 4:
        brain['events']['room']['value'] = 4
        room = "hot"
    elif brain['events']['room']['value'] == 3:
        room = "warm"
    elif brain['events']['room']['value'] == 2:
        room = "mild"
    elif brain['events']['room']['value'] == 1:
        room = "cold"
    else:
        room = "freezing"

    reply = "The fire is {}. The room is {}.".format(
        fire, room
    )
    jenni.write(['NOTICE', msg.sender, ":{}".format(reply)])
    jenni.brain.save()
adr_stoke_fire.rule = r"^(\x01ACTION )stokes (?:the )?fire"
adr_stoke_fire.priority = 'medium'


def adr_gathers_wood(jenni, msg):
    init_adr_brain(jenni)
    now = int(time.time())
    brain = jenni.brain['adr']
    duration = brain['cooldown']['wood']
    if now - brain['inventory']['wood'][-1] < duration:
        remaining = duration - (now - brain['inventory']['wood'][-1])
        jenni.reply("you are currently gathering wood. "
                    "Try again in {} seconds.".format(remaining))
        return
    brain['inventory']['wood'].append(now)
    reply = "You currently have {} wood in your inventory.".format(
        sum([now - x >= duration for x in brain['inventory']['wood']]))
    jenni.write(['NOTICE', msg.sender, ":{}".format(reply)])
    jenni.brain.save()
adr_gathers_wood.rule = r"^(\x01ACTION )(?:gathers|collects) wood"
adr_gathers_wood.priority = 'medium'
