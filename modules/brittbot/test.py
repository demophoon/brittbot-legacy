#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/test.py - Test modules and features

import datetime
import time
import random
import re
from functools import wraps

from dateutil.relativedelta import relativedelta
from textblob import TextBlob

from modules.brittbot.helpers import (
    colorize_msg,
    colorize,
    colors,
    elapsed,
)


def config_print(jenni, msg):
    if not msg.admin:
        return
    reply = colorize_msg("tested. rainbows and stuff.")
    jenni.write(['PRIVMSG', msg.sender, ":{}".format(reply)])
config_print.rule = r"^test$"
config_print.priority = 'medium'


def translate_this(jenni, msg):
    t_msg = TextBlob(msg.groups()[0])
    from_lang = t_msg.detect_language()
    if from_lang != 'en':
        translated = t_msg.translate(from_lang=from_lang, to='en')
        jenni.reply("{}".format(translated))
    else:
        return
translate_this.rule = r'^!translate (.*)$'


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


def diceroll(jenni, msg):
    max_dice = 10
    max_side = 100
    num_of_dice = int(msg.groups()[0])
    num_of_side = int(msg.groups()[1])
    truncate_warning = ""
    if num_of_dice * num_of_side > max_dice * max_side:
        num_of_dice = min(max_dice, int(msg.groups()[0]))
        num_of_side = min(max_side, int(msg.groups()[1]))
        truncate_warning = "Truncating results to {}d{}. ".format(num_of_dice, num_of_side)
    if num_of_side < 1:
        return
    rolls = [random.randint(1, num_of_side) for _ in range(num_of_dice)]
    total = sum(rolls)
    reply = ""
    if msg.groups()[2]:
        if total >= num_of_dice * num_of_side / 2:
            reply = "Roll Succeeds! "
        else:
            reply = "Roll Fails! "
    if len(rolls) > 1:
        reply += "Total: {}, Rolls: {}".format(
            total,
            ', '.join([str(x) for x in rolls])
        )
    else:
        reply += "Roll: {}".format(
            ', '.join([str(x) for x in rolls])
        )
    jenni.reply(truncate_warning + reply)
diceroll.rule = r"^(?:\x01ACTION rolls |!roll |$nickname\W? roll |$nickname\W? |)(\d+)d(\d+)(.*)"


def set_brain_param(jenni, msg):
    if not msg.admin:
        return
    path = msg.groups()[0].strip()
    current_node = jenni.brain
    if path:
        for key in path.split('.'):
            current_node = current_node[key]
    if isinstance(current_node, dict):
        value = ', '.join(current_node.keys())
    elif isinstance(current_node, list):
        value = ', '.join(current_node)
    else:
        value = repr(current_node)

    if new_value:
        if not(isinstance(current_node, int) or isinstance(current_node, str)):
            jenni.reply("Unable to set non int or str values")
            return
        if new_value.isdigit():
            new_value = int(new_value)
        current_node = new_value
        jenni.brain.save()
        jenni.reply("{} is now set to {}".format(path, new_value))
        return
    jenni.reply(value)
set_brain_param.rule = r"^!(read|write)brain(.*)"


def urlshortner(jenni, msg):
    import requests
    from modules.find import load_db

    in_url = msg.groups()[0]
    if not in_url:
        imgs = load_db().get(msg.sender)
        if imgs and 'last_said' in imgs:
            url_regex = "(https?://\S+)"
            for img in reversed(imgs['last_said']):
                urls = re.findall(url_regex, img)
                if urls:
                    in_url = urls[0].strip()
                    break
    if not in_url:
        return
    shrls_server = jenni.config.shrls.get('server')
    shrls_username = jenni.config.shrls.get('username')
    shrls_password = jenni.config.shrls.get('password')
    response = requests.get('{}/admin/create'.format(shrls_server), params={
        'u': in_url,
        'c': jenni.nick,
        'url_only': True,
    }, auth=(shrls_username, shrls_password))
    if response.status_code != 200:
        jenni.reply("An error has occurred.")
        return
    url = response.content
    jenni.say(url)
urlshortner.rule = r'^!(?:shrl|url|shorten|short|shortener)( \S+)?'


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
        jenni.brain.save()
    try:
        rekt = jenni.brain['ofthe'][x][y][msg.sender][-1]
        expires = None
        if isinstance(rekt, dict):
            expires = rekt['expires']
            if time.mktime(now.timetuple()) > expires:
                reply = "I need a new {} of the {}. It was {}.".format(
                    x,
                    y,
                    colorize(rekt['item'], fg=colors['red']),
                )
                jenni.write(['PRIVMSG', msg.sender, ":{}".format(reply)])
                return
            rekt = rekt['item']
    except Exception:
        return
    reply = "The {} of the {} is {}.".format(
        x,
        y,
        colorize(rekt, fg=colors['red']),
    )
    if expires:
        reply += ' (Expires in {})'.format(
            elapsed(expires - time.mktime(now.timetuple())).strip()
        )
    jenni.write(['PRIVMSG', msg.sender, ":{}".format(reply)])
xofthey.rule = r"^!(\w+)ofthe(\w+)( .*)?"


def dayssincelast(jenni, msg):
    item = msg.groups()[0]
    if 'days_since' not in jenni.brain:
        jenni.brain['days_since'] = {}
    if msg.sender not in jenni.brain['days_since']:
        jenni.brain['days_since'][msg.sender] = {}
    if item not in jenni.brain['days_since'][msg.sender]:
        return
    jenni.reply("Days since {}: {}".format(
        item,
        elapsed(
            time.time() - jenni.brain['days_since'][msg.sender][item]
        ),
    ))
dayssincelast.rule = r"^!dayssince (.*)"


def dayssincelastset(jenni, msg):
    item = msg.groups()[0]
    if 'days_since' not in jenni.brain:
        jenni.brain['days_since'] = {}
    if msg.sender not in jenni.brain['days_since']:
        jenni.brain['days_since'][msg.sender] = {}
    jenni.brain['days_since'][msg.sender][item] = time.time()
    jenni.brain.save()
    jenni.reply("Days since {}: {}".format(
        item,
        elapsed(0),
    ))
dayssincelastset.rule = r"^!setdayssince (.*)"


def award_item(jenni, msg):
    groups = msg.groups()
    if groups[0] == 'give':
        modifier = 1
        to = groups[1]
        quantity = groups[2]
        item = groups[3]
    elif groups[0] == 'take':
        modifier = -1
        quantity = groups[1]
        item = groups[2]
        to = groups[3]
        if to.lower().startswith('from '):
            to = ''.join(to.split(' ')[1:])
    to = to.lower().strip()
    item = item.lower().strip()
    quantity = quantity.lower().strip()

    if to[-1] == '\x01':
        to = to[:-1]
    if item[-1] == '\x01':
        item = item[:-1]

    if to == msg.nick:
        return

    # Get Quantity
    doge = quantity in ['many', 'so', 'much', 'such', 'wow']
    if quantity.lower() in ['a', 'an', 'another', 'one', 'the']:
        quantity = 1
    elif quantity.lower() in ['more', 'some', 'many', 'much', 'wow', 'so', 'such', 'lotsa']:
        if item.split(' ')[0] in ['more']:
            item = ' '.join(item.split(' ')[1:])
        quantity = random.choice(range(2, 10))
    elif quantity.lower() in ['all']:
        quantity = 10
        if item.split(' ')[0] == 'the':
            item = ' '.join(item.split(' ')[1:])
        else:
            return
    if quantity.isdigit():
        quantity = int(quantity)

    if quantity > 1:
        if item.endswith('ies'):
            item = item[:-3] + 'y'
        elif item.endswith('es'):
            item = item[:-2]
        elif item.endswith('s'):
            item = item[:-1]

    quantity = quantity * modifier

    if 'award_item' not in jenni.brain:
        jenni.brain['award_item'] = {}
    if msg.sender not in jenni.brain['award_item']:
        jenni.brain['award_item'][msg.sender] = {}
    if to not in jenni.brain['award_item'][msg.sender]:
        jenni.brain['award_item'][msg.sender][to] = {}
    if item not in jenni.brain['award_item'][msg.sender][to]:
        jenni.brain['award_item'][msg.sender][to][item] = 0
    jenni.brain['award_item'][msg.sender][to][item] += quantity
    jenni.brain.save()
    user_points = jenni.brain['award_item'][msg.sender][to][item]

    if user_points != 1:
        if item.endswith('es'):
            pass
        elif item.endswith('y'):
            item = item[:-1] + 'ies'
        elif item.endswith('s') or item.endswith('x'):
            item += 'es'
        else:
            item += 's'

    message = '{} has {} {}.'.format(to, user_points, item)
    if doge:
        message += random.choice([
            ' such {}.'.format(item),
            ' so {}.'.format(item),
            ' wow.',
            ' so amaze.',
            ' many {}.'.format(item),
        ])
    jenni.reply(message)
award_item.rule = r'^(?:!|\x01ACTION )(give|take)s? (\S+) (\S+) (.+)'


def rainbowize(jenni, msg):
    reply = colorize_msg(msg.groups()[0])
    jenni.write(['PRIVMSG', msg.sender, u":{}".format(reply)])
rainbowize.rule = r"^!rainbows?(?:fg)? (.*)"


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
    jenni.write(['PRIVMSG', msg.sender, u":{}".format(final)])
rainbowizebg.rule = r"^!rainbows?bg (.*)"


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
    jenni.write(['PRIVMSG', msg.sender, u":{}".format(final)])
rainbowizefgbg.rule = r"^!rainbows?(?:fgbg|bgfg) (.*)"


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
    jenni.reply(reply.upper())
buzzfeedify.rule = r"^!buzzfeed (.*)"


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


def global_notice(jenni, msg):
    if not msg.admin:
        return
    reply = msg.groups()[0]
    notice_channels = [
        "##brittslittlesliceofheaven",
        "##brittbot",
        "##brittbot-trivia",
    ]
    for chan in notice_channels:
        jenni.write(['NOTICE', chan, ":{}".format(reply)])
global_notice.rule = r"!notice (.*)"
global_notice.priority = 'medium'


def shutdown(jenni, msg):
    if not msg.owner:
        return
    priorities = sorted(jenni.commands.keys())
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
