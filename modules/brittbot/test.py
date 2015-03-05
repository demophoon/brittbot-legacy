#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/test.py - Test modules and features

import datetime
from dateutil.relativedelta import relativedelta
import time
import math
import random

from modules.brittbot.filters import smart_ignore
from modules.brittbot.helpers import (
    colorize_msg,
    colorize,
    colors,
    elapsed
)


def notice(jenni, chan, msg):
    jenni.write(['NOTICE', chan, ":%s" % msg])


@smart_ignore
def config_print(jenni, msg):
    if not msg.admin:
        return
    reply = colorize_msg("tested. rainbows and stuff.")
    jenni.write(['PRIVMSG', msg.sender, ":%s" % reply])
config_print.rule = r"^test$"
config_print.priority = 'medium'


@smart_ignore
def xofthey(jenni, msg):
    now = datetime.datetime.utcnow()
    durations = {
        'millisecond': relativedelta(microseconds=1),
        'microsecond': relativedelta(microseconds=1),
        'second': relativedelta(seconds=1),
        'minute': relativedelta(minutes=1),
        'hour': relativedelta(hours=1),
        'day': relativedelta(days=1),
        'week': relativedelta(weeks=1),
        'month': relativedelta(months=1),
        'year': relativedelta(years=1),
        'decade': relativedelta(years=10),
        'century': relativedelta(years=100),
        'millennium': relativedelta(years=1000),
    }
    x = msg.groups()[0].strip()
    y = msg.groups()[1].strip()
    item = msg.groups()[2]
    if 'ofthe' not in jenni.brain:
        jenni.brain['ofthe'] = {}
    rekt_dict = jenni.brain['ofthe']
    if x not in rekt_dict:
        rekt_dict[x] = {}
    if y not in rekt_dict[x]:
        rekt_dict[x][y] = {}
    if msg.sender not in rekt_dict[x][y]:
        rekt_dict[x][y][msg.sender] = []
    expires = None
    if durations.get(y):
        expires = now + durations.get(y)
    if item:
        if expires:
            rekt_dict[x][y][msg.sender].append({
                'item': item.strip(),
                'created': time.mktime(now.timetuple()),
                'expires': time.mktime(expires.timetuple()),
            })
        else:
            rekt_dict[x][y][msg.sender].append(item.strip())
        jenni.save_brain()
    try:
        rekt = jenni.brain['ofthe'][x][y][msg.sender][-1]
        expires = None
        if isinstance(rekt, dict):
            expires = rekt['expires']
            if time.mktime(now.timetuple()) > expires:
                reply = "I need a new %s of the %s. It was %s." % (
                    x,
                    y,
                    colorize(rekt['item'], fg=colors['red']),
                )
                jenni.write(['PRIVMSG', msg.sender, ":%s" % reply])
                return
            rekt = rekt['item']
    except Exception:
        return
    reply = "The %s of the %s is %s." % (
        x,
        y,
        colorize(rekt, fg=colors['red']),
    )
    if expires:
        reply += ' (Expires in %s)' % (
            elapsed(expires - time.mktime(now.timetuple())).strip()
        )
    jenni.write(['PRIVMSG', msg.sender, ":%s" % reply])
xofthey.rule = r"^!(\w+)ofthe(\w+)( .*)?"


@smart_ignore
def dayssincelast(jenni, msg):
    item = msg.groups()[0]
    if 'days_since' not in jenni.brain:
        jenni.brain['days_since'] = {}
    if msg.sender not in jenni.brain['days_since']:
        jenni.brain['days_since'][msg.sender] = {}
    if item not in jenni.brain['days_since'][msg.sender]:
        return
    jenni.reply("Days since %s: %s" % (
        item,
        elapsed(
            time.time() - jenni.brain['days_since'][msg.sender][item]
        ),
    ))
dayssincelast.rule = r"^!dayssince (.*)"


@smart_ignore
def dayssincelastset(jenni, msg):
    item = msg.groups()[0]
    if 'days_since' not in jenni.brain:
        jenni.brain['days_since'] = {}
    if msg.sender not in jenni.brain['days_since']:
        jenni.brain['days_since'][msg.sender] = {}
    jenni.brain['days_since'][msg.sender][item] = time.time()
    jenni.save_brain()
    jenni.reply("Days since %s: %s" % (
        item,
        elapsed(0),
    ))
dayssincelastset.rule = r"^!setdayssince (.*)"


@smart_ignore
def rainbowize(jenni, msg):
    reply = colorize_msg(msg.groups()[0])
    jenni.write(['PRIVMSG', msg.sender, ":%s" % reply])
    rainbowize.rule = r"^!rainbows?(:?fg)? (.*)"


@smart_ignore
def rainbowizebg(jenni, msg):
    rmsg = msg.groups()[0]
    final = unicode()
    rainbow = [
        'red',
        'orange',
        'yellow',
        'green',
        'cyan',
        'blue',
        'purple',
    ]
    starting_index = random.choice(range(len(rainbow)))
    for index, char in enumerate(rmsg):
        rindex = index + starting_index
        final += colorize(
            char,
            fg=colors['black'],
            bg=colors[rainbow[rindex % len(rainbow)]],
        )
    jenni.write(['PRIVMSG', msg.sender, ":%s" % final])
rainbowizebg.rule = r"^!rainbows?bg (.*)"


@smart_ignore
def rainbowizefgbg(jenni, msg):
    rmsg = msg.groups()[0]
    final = unicode()
    rainbow = [
        'red',
        'orange',
        'yellow',
        'green',
        'cyan',
        'blue',
        'purple',
    ]
    starting_index = random.choice(range(len(rainbow)))
    for index, char in enumerate(rmsg):
        rindex = index + starting_index
        rindexbg = index + starting_index + (len(rainbow) / 2)
        final += colorize(
            char,
            fg=colors[rainbow[rindex % len(rainbow)]],
            bg=colors[rainbow[rindexbg % len(rainbow)]],
        )
    jenni.write(['PRIVMSG', msg.sender, ":%s" % final])
rainbowizefgbg.rule = r"^!rainbows?(?:fgbg|bgfg) (.*)"


@smart_ignore
def ohai(jenni, msg):
    return
    jenni.config.allowed_channels
    jenni.reply("facter")
    pass
ohai.rule = r".*ohai.*"
ohai.priority = 'medium'


@smart_ignore
def eightball(jenni, msg):
    replies = [
        "Signs point to yes.",
        "Yes.",
        "Reply hazy, try again.",
        "Without a doubt.",
        "My sources say no.",
        "As I see it, yes.",
        "You may rely on it.",
        "Concentrate and ask again.",
        "Outlook not so good.",
        "It is decidedly so.",
        "Better not tell you now.",
        "Very doubtful.",
        "Yes - definitely.",
        "It is certain.",
        "Cannot predict now.",
        "Most likely.",
        "Ask again later.",
        "My reply is no.",
        "Outlook good.",
        "Don't count on it.",
    ]
    jenni.reply(random.choice(replies))
eightball.rule = r'^!(eight|8)ball'


@smart_ignore
def cagemebro(jenni, msg):
    replies = [
        "AAHHHHHHHHHHHHHHHHHGGGH!!!!!!!!",
    ]
    jenni.reply(random.choice(replies))
cagemebro.rule = r'^!cageme(bro)?'


@smart_ignore
def global_notice(jenni, msg):
    if not msg.admin:
        return
    reply = msg.groups()[0]
    notice_channels = [
        "##brittslittlesliceofheaven",
        "##brittbot",
    ]
    for chan in notice_channels:
        jenni.write(['NOTICE', chan, ":%s" % reply])
global_notice.rule = r"!notice (.*)"
global_notice.priority = 'medium'


def init_adr_brain(jenni):
    brain = jenni.brain
    adr_version = "1.0.1"
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
        jenni.save_brain()


@smart_ignore
def adr_modify_cooldown(jenni, msg):
    chan, item, duration, message = msg.groups()
    if jenni.brain['adr']['cooldown'].get(item):
        jenni.brain['adr']['cooldown'][item] = int(duration)
        if message:
            jenni.write(['NOTICE', chan, ":%s" % message])
adr_modify_cooldown.rule = r"^!adraward (#*\w+) (\w+) (\d+) (.*)"


@smart_ignore
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


@smart_ignore
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

    if len(brain['inventory']['wood']) > 0:
        brain['inventory']['wood'] = brain['inventory']['wood'][1:]
        brain['events']['fire']['value'] += 1
        brain['events']['fire']['last_update'] = now
        brain['events']['room']['value'] += 1
        brain['events']['room']['last_update'] = now
    else:
        notice(jenni, msg.sender, "Not enough wood to keep the fire going")
        return
    duration = brain['cooldown']['fire']
    elapsed = now - brain['events']['fire']['last_update']
    dv = math.floor(float(elapsed) / float(duration))
    brain['events']['fire']['value'] -= dv
    brain['events']['fire']['value'] = max(0, brain['events']['fire']['value'])
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

    reply = "The fire is %s. The room is %s." % (
        fire, room
    )
    jenni.write(['NOTICE', msg.sender, ":%s" % reply])
    jenni.save_brain()
adr_stoke_fire.rule = r"^(\x01ACTION )stokes (?:the )?fire"
adr_stoke_fire.priority = 'medium'


@smart_ignore
def adr_gathers_wood(jenni, msg):
    init_adr_brain(jenni)
    now = int(time.time())
    brain = jenni.brain['adr']
    duration = brain['cooldown']['wood']
    if now - brain['inventory']['wood'][-1] < duration:
        remaining = duration - (now - brain['inventory']['wood'][-1])
        jenni.reply("you are currently gathering wood. "
                    "Try again in %s seconds." % (remaining))
        return
    brain['inventory']['wood'].append(now)
    reply = "You currently have %s wood in your inventory." % (
        sum([now - x >= duration for x in brain['inventory']['wood']]))
    jenni.write(['NOTICE', msg.sender, ":%s" % reply])
    jenni.save_brain()
adr_gathers_wood.rule = r"^(\x01ACTION )(?:gathers|collects) wood"
adr_gathers_wood.priority = 'medium'


@smart_ignore
def shutdown(jenni, msg):
    if not msg.owner:
        return
    priorities = [
        'high',
        'medium',
        'low',
    ]
    print "Preparing for shutdown!"
    for priority in priorities:
        for pattern in jenni.commands[priority]:
            for fn in jenni.commands[priority][pattern]:
                if fn.__name__ == "shutdown_handler":
                    fn(jenni, msg)
    print "Shutting down"
    jenni.write(['QUIT'])
    __import__('os')._exit(0)
shutdown.rule = r"^!shutdown$"
shutdown.priority = 'high'
