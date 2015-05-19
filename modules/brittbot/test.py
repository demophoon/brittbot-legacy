#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/test.py - Test modules and features

import datetime
from dateutil.relativedelta import relativedelta
import time
import math
import random
import os
import json

from textblob import TextBlob

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
def tacobellitem(jenni, msg):
    from modules.brittbot.tacobell import generate_taco_bell
    vegan = False
    if msg.groups(0) == 'vegan':
        vegan = True
    jenni.reply("You should get the %s." % generate_taco_bell(vegan))
tacobellitem.rule = r"$nickname.*what.*(vegan)?.*taco bell"


@smart_ignore
def mnightwho(jenni, msg):
    reply = "Did you mean M. Night Sha"
    reply += ''.join([random.choice("lamin") for _ in range(random.randint(6,24))])
    reply += 'n?'
    jenni.reply(reply)
mnightwho.rule = r"(?i).*(m\.? night).*"


@smart_ignore
def arewefriends(jenni, msg):
    if msg.friend:
        reply = "Yes"
    else:
        reply = "No"
    jenni.reply(reply)
arewefriends.rule = r"(?i)^$nickname\W? (?:are you my|am i your|are we) friends?\??"


@smart_ignore
def noneed(jenni, msg):
    reply = "http://youtu.be/ygr5AHufBN4"
    jenni.say(reply)
noneed.rule = r"(?i)^!noneed"


@smart_ignore
def xfacts(jenni, msg):
    if 'facts' not in jenni.brain:
        jenni.brain['facts'] = {}
    facttype = msg.groups()[0].lower()
    fact = msg.groups()[1]
    if facttype not in jenni.brain['facts']:
        jenni.brain['facts'][facttype] = []
    if fact and fact.strip():
        jenni.brain['facts'][facttype].append(fact.strip())
        reply = "Fact added."
    else:
        if not jenni.brain['facts'][facttype]:
            return
        reply = random.choice(jenni.brain['facts'][facttype])
    jenni.reply(reply)
xfacts.rule = r"(?i)^!(\w+)facts( .*)?"


@smart_ignore
def alwaysbouttoretto(jenni, msg):
    jenni.brain['alwaysbouttorreto'] = time.time()
    reply = "Is it about Toretto?"
    jenni.reply(reply)
alwaysbouttoretto.rule = r"^$nickname\W? guess what"


@smart_ignore
def alwaysabouttorettoreply(jenni, msg):
    if 'alwaysbouttorreto' in jenni.brain:
        if time.time() - jenni.brain['alwaysbouttorreto'] > 60:
            return
        if not jenni.brain['alwaysbouttorreto']:
            return
    if msg.groups()[0].lower() == 'y':
        reply = "Continue."
    else:
        reply = "I don't care."
    jenni.brain['alwaysbouttorreto'] = False
    jenni.reply(reply)
alwaysabouttorettoreply.rule = r"(?i)^(?:$nickname\W? )?(y|n)\w+"


@smart_ignore
def diceroll(jenni, msg):
    num_of_dice = min(10, int(msg.groups()[0]))
    num_of_side = min(1000, int(msg.groups()[1]))
    rolls = [random.choice(range(1, num_of_side)) for _ in range(num_of_dice)]
    total = sum(rolls)
    reply = ""
    if msg.groups()[2]:
        if total >= num_of_dice * num_of_side / 2:
            reply = "Roll Succeeds! "
        else:
            reply = "Roll Fails! "
    if len(rolls) > 1:
        reply += "Total: %s, Rolls: %s" % (
            total,
            ', '.join([str(x) for x in rolls])
        )
    else:
        reply += "Roll: %s" % (
            ', '.join([str(x) for x in rolls])
        )
    jenni.reply(reply)
diceroll.rule = r"^(?:\x01ACTION rolls |)(\d+)d(\d+)(.*)"


def approval_rating(jenni, msg):
    try:
        analysis = TextBlob(str(msg))
    except Exception:
        return
    if 'approval' not in jenni.brain:
        jenni.brain['approval'] = {}
    if msg.nick not in jenni.brain['approval']:
        jenni.brain['approval'][msg.nick] = 0
    jenni.brain['approval'][msg.nick] += analysis.sentiment.polarity
    jenni.save_brain()
    print "Approval rating from %s: %s (%s)" % (
        msg.nick,
        jenni.brain['approval'][msg.nick],
        analysis.sentiment.polarity,
    )
approval_rating.rule = r".*$nickname.*"


def room_rating(jenni, msg):
    try:
        analysis = TextBlob(str(msg))
    except Exception:
        return
    if 'approval_room' not in jenni.brain:
        jenni.brain['approval_room'] = {}
    if msg.sender not in jenni.brain['approval_room']:
        jenni.brain['approval_room'][msg.sender] = {}
    if msg.nick not in jenni.brain['approval_room'][msg.sender]:
        jenni.brain['approval_room'][msg.sender][msg.nick] = 0
    if analysis.sentiment.subjectivity < .5:
        return
    jenni.brain['approval_room'][msg.sender][msg.nick] += analysis.sentiment.polarity
    if not analysis.sentiment.polarity == 0:
        jenni.save_brain()
        p = analysis.sentiment.polarity
        if p > 0:
            p = "+%0.2f" % (p, )
        else:
            p = "%0.2f" % (p, )
        print "%s <%s> (%s, %0.2f): %s" % (
            msg.sender,
            msg.nick,
            p,
            jenni.brain['approval_room'][msg.sender][msg.nick],
            msg,
        )
room_rating.rule = r".*"


@smart_ignore
def how_happy_is_room(jenni, msg):
    if not msg.admin:
        return
    room = msg.groups()[0]
    final_score = 0
    highest_score = 0
    highest_user = None
    lowest_score = 0
    lowest_user = None
    if room in jenni.brain['approval_room']:
        for user in jenni.brain['approval_room'][room]:
            score = jenni.brain['approval_room'][room][user]
            if not (highest_user and lowest_user):
                highest_user = user
                highest_score = score
                lowest_user = user
                lowest_score = score
            if score > highest_score:
                highest_score = score
                highest_user = user
            if score < lowest_score:
                lowest_score = score
                lowest_user = user
            final_score += score
        reply = room
        if final_score > 0:
            reply += " is generally a positive room"
        else:
            reply += " is generally a negative room"
        reply += " (%0.2f)." % (final_score, )
        reply += " The most positive person in the room is %s (%0.2f) and " % (
            highest_user,
            highest_score,
        )
        reply += "it seems the most negative person in the room is %s (%0.2f)." % (
            lowest_user,
            lowest_score,
        )
    elif room in jenni.brain['approval_room'][msg.sender]:
        reply = "%s approval score is %s." % (
            room,
            '%0.2f' % (jenni.brain['approval_room'][msg.sender][room]),
        )
    jenni.reply(reply)
how_happy_is_room.rule = r"!approval (\S+)"


@smart_ignore
def how_happy_am_i(jenni, msg):
    room = msg.sender
    nick = msg.nick
    approvals = jenni.brain['approval_room'][room]
    approvals[msg.nick],
    if nick not in approvals:
        return
    score = approvals[nick]
    jenni.reply("Your approval score is: %0.2f" % score)
how_happy_am_i.rule = r"!approval$"


@smart_ignore
def reload_brain(jenni, msg):
    if not msg.admin:
        return
    if not os.path.isfile(jenni.brain_file):
        jenni.brain = {}
        jenni.save_brain()
    f = open(jenni.brain_file, 'r')
    jenni.brain = json.loads(f.read())
    f.close()
    jenni.reply("brain reloaded.")
reload_brain.rule = r"^!loadbrain"


@smart_ignore
def justxthingshandler(jenni, msg):
    from modules.brittbot.pil import justxthings
    hashtag = msg.groups()[1]
    quote = msg.groups()[0]

    if quote[0] in ['!']:
        return
    if hashtag.startswith("##"):
        return
    url = "http://brittbot.brittg.com/%s" % justxthings.generate_image(
        str(quote),
        hashtag,
    )
    jenni.reply(url)
justxthingshandler.rule = r"(.*) (#\S+\w)$"


@smart_ignore
def justxthingslistener(jenni, msg):
    from modules.brittbot.pil import justxthings
    if msg.sender not in [
        "#internship",
        "#r/kansascity",
        "#reddit-stlouis",
        "demophoon",
    ]:
        return
    if 'last_action' not in jenni.brain:
        jenni.brain['last_action'] = {}
    if msg.sender not in jenni.brain['last_action']:
        jenni.brain['last_action'][msg.sender] = 0
    if time.time() < jenni.brain['last_action'][msg.sender] + 3600:
        return
    if len(msg.split(' ')) == 1 or len(msg.split(' ')) > 20:
        return
    try:
        if str(msg)[0] in ['!']:
            return
    except Exception:
        return

    if random.choice(range(175)) == 0:
        url = "http://brittbot.brittg.com/%s" % justxthings.generate_image(
            str(msg),
            "#just%sthings" % (msg.nick, )
        )
        jenni.say(url)
        jenni.brain['last_action'][msg.sender] = time.time()
justxthingslistener.rule = r".*"


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
    if x == 'gay':
        return
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
    print msg.groups()
    reply = colorize_msg(msg.groups()[0])
    jenni.write(['PRIVMSG', msg.sender, ":%s" % reply])
rainbowize.rule = r"^!rainbows?(?:fg)? (.*)"


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
def correct_me(jenni, msg):
    pass
correct_me.rule = r".*$nickname.*"


@smart_ignore
def buzzfeedify(jenni, msg):
    subjects = TextBlob(str(msg)).noun_phrases.pluralize()
    if subjects:
        subject = random.choice(subjects)
    else:
        subject = msg.groups()[0]
    random_number = random.choice(range(300))
    people = [
        'you',
        'your dog',
        'your cat',
        'your mom',
        'your dad',
        'your mother',
        'your father',
        'your coworker',
    ]
    is_are = [
        'could possibly be',
        'are not',
        'could not possibly be',
        'are actually',
        'are literally',
    ]
    actions = [
        'Russian cosmonauts',
        'eating these cookies',
        'fake',
        'lizard people',
        'what your worst nightmares are made of',
        'completely wrong',
        'literally cannot even',
    ]
    actions += people
    switch = random.choice(['count'])
    if switch == 'count':
        saying = ["%(count)s"]
        qualifiers = [
            'annoying',
            'irritating',
            'dangerous',
            'realistic',
            'unimaginative',
            'amazing',
            'cutest',
        ]
        things = [
            'things',
            'reasons',
            'ideas',
        ]
        saying.append('of the most')
        saying.append(random.choice(qualifiers))
        saying.append(random.choice(things))
        saying.append('why')
        saying.append('%(subject)s')
        saying.append(random.choice(is_are))
        saying.append(random.choice(actions))
        if random.choice([True, False]):
            saying[-1] += '.'
            you_wont_believe = [
                "Just wait until until you get to #%(justwait)s.",
                "You won't believe #%(justwait)s.",
                "I cannot believe #%(justwait)s.",
            ]
            saying.append(random.choice(you_wont_believe))
        saying = ' '.join(saying)
    reply = saying % {
        'subject': subject,
        'count': random_number,
        'justwait': random.choice(range(random_number)),
    }
    jenni.reply(reply)
buzzfeedify.rule = r"^!buzzfeed (.*)"


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
