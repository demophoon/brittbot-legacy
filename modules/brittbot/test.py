#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/test.py - Test modules and features

import datetime
from dateutil.relativedelta import relativedelta
import time
import math
import random
import os
import re
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
    jenni.write(['NOTICE', chan, ":{}".format(msg)])


@smart_ignore
def config_print(jenni, msg):
    if not msg.admin:
        return
    reply = colorize_msg("tested. rainbows and stuff.")
    jenni.write(['PRIVMSG', msg.sender, ":{}".format(reply)])
config_print.rule = r"^test$"
config_print.priority = 'medium'


@smart_ignore
def tacobellitem(jenni, msg):
    from modules.brittbot.tacobell import generate_taco_bell
    vegan = False
    if msg.groups(0) == 'vegan':
        vegan = True
    drinks = ["Mtn Dew Baja Blast"]
    items = []
    for _ in range(random.randint(1, 3)):
        items.append(generate_taco_bell(vegan))
    if len(items) <= 2 and random.randint(1, 11) == 1:
        items.append(random.choice(drinks))
    if len(items) > 1:
        saying = ", a ".join(items[:-1]) + ", and a " + items[-1]
    else:
        saying = items[0]
    jenni.reply("You should get a {}.".format(saying))
tacobellitem.rule = r"$nickname.*(what)?.*(vegan)?.*taco bell\?"


@smart_ignore
def how_many_x(jenni, msg):
    many = msg.groups()[0]
    subjects = TextBlob(str(msg.groups()[1])).noun_phrases.pluralize()
    if subjects:
        subject = random.choice(subjects)
        many = "many"
    else:
        subject = msg.groups()[1]
    if subject and len(subject.split(" ")) > 3:
        return
    if not subject:
        subject = ""
    so = "so"
    if subject == "cooks":
        so = "too"
        many = "many"
    if "second" in subject:
        so = "just"
        many = "one"
        subject = "second"
    if "fuck" in subject:
        so = "no"
        many = "fucks"
        subject = "given"
    if "brittbot" in subject.lower().split(" "):
        subject = subject.lower().replace("brittbot", msg.nick.lower())
    elif "i" in subject.lower().split(" "):
        subject = subject.lower().replace("i", "you")
    jenni.say("{} {} {}".format(so, many, subject))
how_many_x.rule = r"(?i)how (few|many|much) ?([a-zA-Z\s]+)?\??$"


@smart_ignore
def translate_this(jenni, msg):
    t_msg = TextBlob(msg.groups()[0])
    from_lang = t_msg.detect_language()
    if from_lang != 'en':
        translated = t_msg.translate(from_lang=from_lang, to='en')
        jenni.reply("{}".format(translated))
    else:
        return
translate_this.rule = r'^!translate (.*)$'


@smart_ignore
def mnightwho(jenni, msg):
    reply = "Did you mean M. Night Sha"
    reply += ''.join([random.choice("shlamin") for _ in range(random.randint(6,24))])
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
def alot(jenni, msg):
    print msg
    if "a alot" in msg or "an alot" in msg:
        return
    reply = "http://brittg.com/alot"
    jenni.say("I think you mean 'a lot', {}".format(reply))
alot.rule = r"(?i).* alot .*"


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
    jenni.brain.save()
    print "Approval rating from {}: {} ({})".format(
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
        jenni.brain['approval_room'][msg.sender][msg.nick] = {'msgs': 0, 'score': 0}
    if analysis.sentiment.subjectivity < .5:
        return
    jenni.brain['approval_room'][msg.sender][msg.nick]['msgs'] += 1
    jenni.brain['approval_room'][msg.sender][msg.nick]['score'] += analysis.sentiment.polarity
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
            if jenni.brain['approval_room'][room][user]['msgs'] <= 25:
                continue
            score = jenni.brain['approval_room'][room][user]['score'] / jenni.brain['approval_room'][room][user]['msgs']
            score *= 100
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
        score = jenni.brain['approval_room'][msg.sender][room]['score'] / jenni.brain['approval_room'][msg.sender][room]['msgs']
        score *= 100
        reply = "{} approval score is {}.".format(
            room,
            '%0.2f' % (score),
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
    if approvals[nick]['msgs'] <= 0:
        return
    samples = approvals[nick]['msgs']
    score = approvals[nick]['score'] / samples
    score *= 100
    jenni.reply("Your approval score is: %0.2f with %s samples" % (score, samples))
how_happy_am_i.rule = r"!approval$"


@smart_ignore
def reload_brain(jenni, msg):
    if not msg.admin:
        return
    if not os.path.isfile(jenni.brain_file):
        jenni.brain = {}
        jenni.brain.save()
    f = open(jenni.brain_file, 'r')
    jenni.brain = json.loads(f.read())
    f.close()
    jenni.reply("brain reloaded.")
reload_brain.rule = r"^!loadbrain"


@smart_ignore
def img_enhance(jenni, msg):
    from modules.brittbot.pil import enhance
    from modules.find import load_db, save_db
    url = msg.groups()[0]
    if not url:
        imgs = load_db().get(msg.sender)
        if imgs and 'last_said' in imgs:
            url_regex = "(https?://\S+\.(?:jpg|png|jpeg|gif))"
            for img in reversed(imgs['last_said']):
                urls = re.findall(url_regex, img)
                if urls:
                    url = random.choice(urls)
                    break
    if not url:
        return
    filename = enhance.enhance(url)
    url = "http://brittbot.brittg.com/{}".format(filename)
    msgs = load_db()
    msgs[msg.sender]['last_said'].append(url)
    save_db(msgs)
    jenni.reply(url)
img_enhance.rule = r'^!enhance( \S+)?$'


@smart_ignore
def img_zoom(jenni, msg):
    from modules.brittbot.pil import enhance
    from modules.find import load_db, save_db
    url = msg.groups()[0]
    if not url:
        imgs = load_db().get(msg.sender)
        if imgs and 'last_said' in imgs:
            url_regex = "(https?://\S+\.(?:jpg|png|jpeg|gif))"
            for img in reversed(imgs['last_said']):
                urls = re.findall(url_regex, img)
                if urls:
                    url = random.choice(urls)
                    break
    if not url:
        return
    filename = enhance.zoom(url)
    url = "http://brittbot.brittg.com/{}".format(filename)
    msgs = load_db()
    msgs[msg.sender]['last_said'].append(url)
    save_db(msgs)
    jenni.reply(url)
img_zoom.rule = r'^!zoom( \S+)?$'


@smart_ignore
def deepdream(jenni, msg):
    import requests
    from requests_toolbelt import MultipartEncoder
    import urllib
    import uuid
    from modules.find import load_db, save_db
    if 'last_trip' in jenni.brain and time.time() - jenni.brain['last_trip'] < 30:
        jenni.reply('Tripping too hard right now, please try again in 30 seconds.')
        return
    in_url = msg.groups()[0]
    if not in_url:
        imgs = load_db().get(msg.sender)
        if imgs and 'last_said' in imgs:
            url_regex = "(https?://\S+\.(?:jpg|jpeg))"
            for img in reversed(imgs['last_said']):
                urls = re.findall(url_regex, img)
                if urls:
                    in_url = random.choice(urls)
                    break
    if not in_url:
        return
    f = open('/tmp/img.jpg', 'wb')
    f.write(urllib.urlopen(in_url).read())
    f.close()
    data = MultipartEncoder({
        'title': 'wat',
        'description': 'none',
        'filter': 'trippy',
        'submit': "Let's Dream",
        'image': ('img0.jpg', open('/tmp/img.jpg', 'rb'), 'image/jpeg'),
    })
    response = requests.post(
        'https://dreamscopeapp.com/api/images',
        data=data,
        verify=False,
        headers={
            'Content-Type': data.content_type
        }
    )
    if response.status_code >= 400:
        print response
        print response.content
        jenni.reply("An error has occurred.")
    image_id = re.findall(r'pageUrl\(\'(\S+)\'\)', response.text)[-1]
    for _ in range(15):
        time.sleep(1.5)
        r = requests.get('https://dreamscopeapp.com/api/images/{}'.format(image_id))
        final_url = r.json()['filtered_url']
        if final_url:
            break
    if not final_url:
        jenni.reply('Deep dream took too long to complete. Try a smaller image.')
        return
    jenni.brain['last_trip'] = time.time()
    img = urllib.urlopen(final_url).read()
    imagepath = '/var/www/htdocs/brittbot/'
    imagename = "%s.jpg" % str(uuid.uuid4()).replace('-', '')[0:8]
    f = open(imagepath + imagename, 'w')
    f.write(img)
    f.close()
    url = "http://brittbot.brittg.com/{}".format(imagename)
    msgs = load_db()
    msgs[msg.sender]['last_said'].append(url)
    save_db(msgs)
    jenni.reply(url)
deepdream.rule = r'^!(?:lsd|deepdream)( \S+)?'


@smart_ignore
def justxthingshandler(jenni, msg):
    from modules.brittbot.pil import justxthings
    from modules.find import load_db

    hashtag = msg.groups()[1]
    quote = msg.groups()[0]

    if not quote:
        quotes = load_db().get(msg.sender)
        if quotes and 'last_said' in quotes:
            quotes['last_said'] = [quote for quote in quotes['last_said'] if not re.match(r'(.*)(#\S+\w)$', quote)]
            quote = ''.join(quotes['last_said'][-1].split(':')[1:])

    if quote[0] in ['!'] or 'http' in quote:
        return

    if hashtag.startswith("##"):
        return
    if len(quote.split(' ')) > 25:
        return
    url = "http://brittbot.brittg.com/{}".format(justxthings.generate_image(
        str(quote),
        hashtag,
    ))
    jenni.reply(url)
justxthingshandler.rule = r"(.*)(#\S+\w)$"


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
        url = "http://brittbot.brittg.com/{}".format(justxthings.generate_image(
            str(msg),
            "#just{}things".format(msg.nick)
        ))
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


@smart_ignore
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


@smart_ignore
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


@smart_ignore
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
        quantity = random.choice(range(2,10))
    elif quantity.lower() in ['all']:
        quantity = 10
        if item.split(' ')[0] == 'the':
            item = ' '.join(item.split(' ')[1:])
        elif quantity.isdigit():
            quantity = int(quantity)
        else:
            return

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


@smart_ignore
def rainbowize(jenni, msg):
    reply = colorize_msg(msg.groups()[0])
    jenni.write(['PRIVMSG', msg.sender, ":{}".format(reply)])
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
    jenni.write(['PRIVMSG', msg.sender, ":{}".format(final)])
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
    jenni.write(['PRIVMSG', msg.sender, ":{}".format(final)])
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
    jenni.reply(reply.upper())
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
        jenni.write(['NOTICE', chan, ":{}".format(reply)])
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
        jenni.brain.save()


@smart_ignore
def adr_modify_cooldown(jenni, msg):
    chan, item, duration, message = msg.groups()
    if jenni.brain['adr']['cooldown'].get(item):
        jenni.brain['adr']['cooldown'][item] = int(duration)
        if message:
            jenni.write(['NOTICE', chan, ":{}".format(message)])
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

    reply = "The fire is {}. The room is {}.".format(
        fire, room
    )
    jenni.write(['NOTICE', msg.sender, ":{}".format(reply)])
    jenni.brain.save()
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
                    "Try again in {} seconds.".format(remaining))
        return
    brain['inventory']['wood'].append(now)
    reply = "You currently have {} wood in your inventory.".format(
        sum([now - x >= duration for x in brain['inventory']['wood']]))
    jenni.write(['NOTICE', msg.sender, ":{}".format(reply)])
    jenni.brain.save()
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
