#!/usr/bin/env python
# encoding: utf-8

return

import datetime
import random
import re
import collections
import urllib
import urllib2
import json

high_five_avail = False
current_high_five = None


def setup(phenny):
    global DBSession
    global Base
    pass


highfives = [
    {
        "type": "raises his hand for a high five.",
        "value": 1,
    },
    {
        "type": "throws his hand down for a low five.",
        "value": 1,
    },
    {
        "type": "shoots his hand up for a high five.",
        "value": 1,
    },
    {
        "type": "throws up his hand and waits for a high five.",
        "value": 1,
    },
    {
        "type": "throws down his hand and waits for a low five.",
        "value": 1,
    },
    {
        "type": "throws both hands in the air for a double high five!",
        "value": 2,
        "response": "gives %(nick)s a double high five and two %(item)s seeing that they now have %(points)d %(item)s.",
    },
]


def ask_for_highfive(phenny):
    global high_five_avail
    global current_high_five
    global highfives
    high_five_avail = True
    current_high_five = random.choice(highfives)
    phenny.say(action(current_high_five['type']))


#def logger(phenny, input):
#    if not DBSession.query(User).filter(User.nick == input.nick).first():
#        new_user = User()
#        new_user.nick = input.nick
#        DBSession.add(new_user)
#    if not DBSession.query(Room).filter(Room.name == input.sender).first():
#        new_room = Room()
#        new_room.name = input.sender
#        DBSession.add(new_room)
#    user_id = DBSession.query(User).filter(User.nick == input.nick).first()
#    room_id = DBSession.query(Room).filter(
#        Room.name == input.sender).first()
#    msg = Message()
#    msg.body = input
#    msg.user_id = user_id.id
#    msg.room_id = room_id.id
#    DBSession.add(msg)
#    DBSession.flush()
#    DBSession.commit()
#
#    last_messages = DBSession.query(Message).join(Room).filter(
#        Room.name==input.sender
#    ).order_by(
#        Message.created_at.desc()
#    ).limit(10).all()
#
#    common = collections.Counter([x.body.strip() for x in last_messages]).most_common(1)
#    if common[0][0] == input.strip() and common[0][1] >= 2 + random.choice(range(3)):
#        if random.choice(range(10)) == 0:
#            phenny.say(common[0][0])
#
#    if input.sender in limited_channels:
#        return
#    if u"┻━" in input and u"━┻" in input:
#        table_length = input.count(u"━")
#        table_str = u""
#        if table_length > 10:
#            table_str = u"━*%d" % table_length
#        else:
#            table_str = u"".join([u"━" for _ in range(table_length)])
#        phenny.say(u"┬" + table_str + u"┬﻿ ノ( ゜-゜ノ)")
#    elif not(high_five_avail) and random.choice(range(500)) == 0:
#        ask_for_highfive(phenny)
#
#logger.rule = r'(.*)'
#logger.priority = 'low'
#logger.thread = False


grab_yourself_warnings = [
    "You cannot grab yourself sicko!",
    "You gotta grab someone else.",
    "Think about what you are doing before you do that.",
    "Lets think about this now...",
    "You cannot grab yourself.",
    "It's better when someone else grabs you.",
]


@smart_ignore
def grab(phenny, input):
    target = input.groups()[1]
    offset = 0
    if offset:
        offset = int(input.groups()[2])
    if target == input.nick:
        phenny.say(random.choice(grab_yourself_warnings))
    elif target == phenny.nick:
        phenny.say("I cannot let you do that.")
    else:
        message = DBSession.query(Message).join(User).join(Room).filter(
            User.nick.ilike("%s%%" % target)
        ).filter(
            Room.name == input.sender
        ).filter(
            not_(Message.body.like("!%"))
        ).order_by(Message.created_at.desc()).limit(1 + offset).all()
        if not message:
            phenny.say("I don't remember what %s said. :(" % target)
        else:
            message = message[int(offset)]
            grabber_user = DBSession.query(User).filter(
                User.nick.ilike("%s%%" % input.nick)
            ).order_by(User.nick.asc()).first()
            new_quote = Quote()
            new_quote.message_id = message.id
            new_quote.grabbed_by = grabber_user.id
            DBSession.add(new_quote)
            DBSession.flush()
            DBSession.commit()
            phenny.say("Quote %d added" % new_quote.id)
grab.rule = r'^(!|\x01ACTION )grabs? ([a-zA-Z0-9-_`]+)\s*-?([0-9]+)?'
grab.priority = 'medium'
grab.thread = False


@smart_ignore
def tag(phenny, input):
    target = input.groups()[1]
    offset = input.groups()[2] or 0
    if target == input.nick:
        phenny.say(random.choice(grab_yourself_warnings))
    elif target == phenny.nick:
        phenny.say("I cannot let you do that.")
    else:
        message = DBSession.query(Message).join(User).join(Room).filter(
            User.nick.ilike("%s%%" % target)
        ).filter(
            Room.name == input.sender
        ).filter(
            not_(Message.body.like("!%"))
        ).order_by(Message.created_at.desc()).all()
        if not message:
            phenny.say("I don't remember what %s said. :(" % target)
        else:
            message = message[int(offset)]
            grabber_user = DBSession.query(User).filter(
                User.nick.ilike("%s%%" % input.nick)
            ).order_by(User.nick.asc()).first()
            new_quote = Quote()
            new_quote.message_id = message.id
            new_quote.grabbed_by = grabber_user.id
            DBSession.add(new_quote)
            DBSession.flush()
            DBSession.commit()
            phenny.say("Quote %d added" % new_quote.id)
grab.rule = r'^(!|\x01ACTION )grabs? ([a-zA-Z0-9-_]+)\s*-?([0-9]+)?'
grab.priority = 'medium'
grab.thread = False


@smart_ignore
def random_quote(phenny, input):
    quote = DBSession.query(Quote).join(
        Message
    ).join(User).join(Room).filter(
        Room.name == input.sender
    ).order_by(
        sa.func.random()
    ).first()
    if quote:
        phenny.say("Quote #%d grabbed by %s: <%s> %s" % (
            quote.id,
            quote.who_grabbed.nick,
            quote.message.user.nick,
            quote.message.body
        ))

random_quote.rule = r'^!random$'
random_quote.priority = 'medium'
random_quote.thread = False


@smart_ignore
def no_context(phenny, input):
    if input.groups():
        target = input.groups()[0]
        msg = DBSession.query(Message).join(Room).filter(
            Room.name == input.sender
        ).filter(
            Message.body.ilike("%%%s%%" % target)
        )
    else:
        msg = DBSession.query(Message).join(Room).filter(
            Room.name == input.sender
        )
    msg = msg.filter(not_(Message.body.like("!%")))
    msg = msg.order_by(
        sa.func.random()
    ).first()
    if msg:
        phenny.say(msg.body)
no_context.rule = r'^!nocontext\s?(.*)'
no_context.priority = 'medium'
no_context.thread = False


@smart_ignore
def random_user_quote(phenny, input):
    target = input.groups()[0]
    quote = DBSession.query(Quote).join(
        Message
    ).join(User).join(Room).filter(
        Room.name == input.sender
    ).filter(
        User.nick.ilike("%s%%" % target)
    ).order_by(
        sa.func.random()
    ).first()
    if quote:
        phenny.say("Quote #%d grabbed by %s: <%s> %s" % (
            quote.id,
            quote.who_grabbed.nick,
            quote.message.user.nick,
            quote.message.body
        ))
    else:
        phenny.say("No quotes from %s" % target)

random_user_quote.rule = r'^!random ([a-zA-Z0-9-_]+)'
random_user_quote.priority = 'medium'
random_user_quote.thread = False


@smart_ignore
def fetch_quote(phenny, input):
    input = re.search(fetch_quote.rule, input.group())
    if not input:
        return
    target = input.groups()[0]
    quote = DBSession.query(Quote).join(
        Message
    ).join(User)
    if target.isdigit():
        quote = DBSession.query(Quote).filter(
            Quote.id == int(target)
        ).first()
    else:
        quote = quote.filter(
            Message.body.ilike("%%%s%%" % target)
        ).first()
    if quote:
        phenny.say("Quote #%d grabbed by %s: <%s> %s" % (
            quote.id,
            quote.who_grabbed.nick,
            quote.message.user.nick,
            quote.message.body
        ))
    else:
        phenny.say("Quote does not exist.")
fetch_quote.rule = r'^!quote (.*)'
fetch_quote.priority = 'medium'
fetch_quote.thread = False


@smart_ignore
def word_count(phenny, input):
    target = input.groups()[0]
    wc = " ".join([x.body for x in DBSession.query(
        Message
    ).join(
        Room
    ).filter(
        not_(Message.body.ilike("!%"))
    ).filter(
        Room.name == input.sender
    ).all()]).lower().count(target.lower())
    phenny.say("%s: Word count for %s: %d" % (
        input.nick,
        target,
        wc,
    ))
word_count.rule = r'^!wc (.*)$'
word_count.priority = 'medium'
word_count.thread = False


def points(phenny, input):
    input = re.search(points.rule, input.group())
    if not input:
        return
    target = input.groups()[1]
    if target.lower() in ["everyone", "everybody"]:
        all_points = sorted(DBSession.query(
            sa.func.sum(Point.value),
            Point.type,
            User.nick,
        ).join(User, Point.user_id == User.id).group_by(
            User.nick
        ).group_by(
            Point.type
        ).order_by(Point.value).all(), reverse=True)[:10]
        phenny.say("Top 10 for %s: %s" % (
            "Everybody",
            ", ".join(["%(nick)s (%(points)d: %(type)s)" % {
                "nick": x[2],
                "points": x[0],
                "type": x[1],
            } for x in all_points])
        ))
        return
    user = DBSession.query(User).filter(
        User.nick.ilike("%s%%" % target)
    ).order_by(User.nick.asc()).first()
    if not user:
        return
    user_points = {}
    for pt in [(x.type, x.value) for x in user.points]:
        if pt[0] not in user_points:
            user_points[pt[0]] = 0
        user_points[pt[0]] += pt[1]
    user_points = collections.Counter(user_points)

    phenny.say("Top 10 for %s: %s" % (
        user.nick,
        ", ".join(["%s (%d)" % x for x in user_points.most_common(10)])
    ))
points.rule = r'^!(point|score|inventory)s? ([a-zA-Z0-9-_]+)'
points.priority = 'medium'
points.thread = False


def last_active(phenny, input):
    target = input.groups()[1]
    user = DBSession.query(User).join(Message).join(
        Room
    ).filter(
        Room.name == input.sender
    ).filter(
        User.nick.ilike("%s%%" % target)
    ).order_by(User.nick.asc()).first()
    message = DBSession.query(Message).join(User).join(
        Room
    ).filter(
        Room.name == input.sender
    ).filter(
        User.nick.ilike("%s%%" % target)
    ).order_by(Message.created_at.desc()).first()
    if not user:
        return
    if user.nick == input.nick:
        phenny.say("Stahp Et >:(")
        return
    delta = get_current_time() - message.created_at
    phenny.say("User %s last message was %sago: %s" % (
        user.nick,
        duration(delta),
        message.body,
    ))
last_active.rule = r'^!(active|last) ([a-zA-Z0-9-_]+)'
last_active.priority = 'medium'
last_active.thread = False


#def leaderboard(phenny, input):
#    user_points = DBSession.query(sa.func.sum(Point.value)).join(User).filter(
#        Point.type == 'respect'
#    ).filter(User.nick == input.nick).all()
#    phenny.say("%s now has %d respect." % (user_id.nick, user_points))
#leaderboard.rule = r'^!leaderboard$'
#leaderboard.priority = 'medium'
#leaderboard.thread = False


@smart_ignore
def give_highfive(phenny, input):
    global high_five_avail
    global current_high_five
    if not high_five_avail:
        return

    input = re.search(give_highfive.rule, input.group())
    if not input:
        return
    highfive_type = input.groups()[0]

    regex = re.compile(" an? ([a-zA-Z- ]+) five")
    r = regex.search(current_high_five['type'])
    matching_type = r.groups()[0]
    if not highfive_type == matching_type:
        return

    user_id = DBSession.query(User).filter(User.nick == input.nick).first()
    awarded_by = user_id
    if user_id:
        DBSession.add(Point("high five", user_id.id, awarded_by.id, current_high_five['value']))
        DBSession.flush()
        DBSession.commit()
        points = DBSession.query(Point).join(
            User, Point.user_id == User.id
        ).filter(
            Point.type == "high five"
        ).filter(User.nick == input.nick).all()
        user_points = 0
        for point in points:
            user_points += point.value

        item = "beers"
        if user_points == 1:
            item = "beer"
        a_an = "a"
        if highfive_type[0] in ['a', 'e', 'i', 'o', 'u']:
            a_an = "an"
        if "response" in current_high_five:
            hf = current_high_five['response']
        else:
            hf = "gives %(nick)s %(a_an)s %(type)s five and sees that they have %(points)d %(item)s"
        hf %= {
            "nick": input.nick,
            "a_an": a_an,
            "type": highfive_type,
            "points": user_points,
            "item": item,
        }
        phenny.msg(input.sender, action(hf))
        high_five_avail = False
        current_high_five = None
give_highfive.rule = r'^\x01ACTION gives $nickname an? ([a-zA-Z- ]+) five'
give_highfive.priority = 'medium'
give_highfive.thread = False


@smart_ignore
def user_point(phenny, input):
    matches = input
    modifier = 1
    if not matches or not matches.groups():
        return
    if matches.groups()[1] == "give":
        regex = r'gives? ([a-zA-Z0-9-_]+) (\w+|-?\d+) ([a-zA-Z0-9,\- ]+)'
        matches = re.search(regex, input.group())
        if not matches:
            return
        target = matches.groups()[0]
        quantity = matches.groups()[1]
        point_type = matches.groups()[2].lower()
    else:
        regex = r'take (\w+|-?\d+) ([a-zA-Z0-9,\- ]+) from ([a-zA-Z0-9-_]+)'
        matches = re.search(regex, input.group())
        if not matches:
            return
        target = matches.groups()[2]
        quantity = matches.groups()[0]
        point_type = matches.groups()[1].lower()
        modifier = -1

    banned_types = ['respect', 'high five']
    if point_type in banned_types:
        return

    doge = quantity in ["many", "so", "much", "such", "wow"]
    if quantity.lower() in ["a", "an", "another", "one", "the"]:
        quantity = 1
    elif quantity.lower() in ["some", "many", "much", "wow", "so", "such", "lotsa"]:
        quantity = random.choice(range(2,10))
    elif quantity.lower() in ["all"]:
        quantity = 10
        if point_type.split(" ")[0] == "the":
            point_type = " ".join(point_type.split(" ")[1:])
    else:
        try:
            quantity = int(quantity)
        except Exception:
            return
    if quantity > 1:
        if point_type.endswith("ies"):
            point_type = point_type[:-3] + "y"
        elif point_type.endswith("es"):
            point_type = point_type[:-2]
        elif point_type.endswith("s"):
            point_type = point_type[:-1]
    if abs(quantity) > 10:
        phenny.say("Woah there buddy, slow down.")
        return
    quantity *= modifier
    awarded_by = DBSession.query(User).filter(User.nick.ilike("%s%%" % input.nick)).first()
    if target.lower() in ["everyone", "everybody"]:
        start_time = get_current_time() - datetime.timedelta(hours=4)
        points = [Point(point_type, x.id, awarded_by.id, quantity) for x in DBSession.query(
            User
        ).join(Message).join(Room).filter(
            Room.name == input.sender
        ).filter(
            Message.created_at > start_time
        ).distinct().all()]
        DBSession.add_all(points)
        DBSession.flush()
        DBSession.commit()
        phenny.say("Done! ^.^")
    elif not(target == input.nick) and point_type not in banned_types:
        user_id = DBSession.query(User).filter(User.nick.ilike("%s%%" % target)).first()
        if user_id:
            DBSession.add(Point(point_type, user_id.id, awarded_by.id, quantity))
            DBSession.flush()
            DBSession.commit()
            points = DBSession.query(Point).join(
                User, Point.user_id == User.id
            ).filter(
                Point.type == point_type
            ).filter(User.nick.ilike("%s%%" % target)).all()
            user_points = 0
            for point in points:
                user_points += point.value
            if not(user_points == 1):
                if point_type.endswith("es"):
                    pass
                elif point_type.endswith("y"):
                    point_type = point_type[:-1] + "ies"
                elif point_type.endswith("s") or point_type.endswith("x"):
                    point_type += "es"
                else:
                    point_type += "s"
            message = "%s has %d %s." % (user_id.nick, user_points, point_type)
            if doge:
                message += random.choice([
                    " such %s." % point_type,
                    " so %s." % point_type,
                    " wow.",
                    " so amaze.",
                    " many %s." % point_type,
                ])
            phenny.say(message)
user_point.rule = r'^(!|\x01ACTION )(give|take)s? (.+)'
user_point.priority = 'medium'
user_point.thread = False


@smart_ignore
def transfer(phenny, input):
    if not input.owner:
        return
    src_user = DBSession.query(User).filter(
        User.nick.ilike("%s%%" % input.groups()[0])
    ).order_by(User.nick.asc()).first()
    dest_user = DBSession.query(User).filter(
        User.nick.ilike("%s%%" % input.groups()[1])
    ).order_by(User.nick.asc()).first()
    if not all([src_user, dest_user]):
        phenny.say("Unable to complete command.")
        return
    all_points = DBSession.query(Point).filter(
        Point.user_id == src_user.id
    ).all()
    updates = []
    for point in all_points:
        point.user_id = dest_user.id
        updates.append(point)
    DBSession.add_all(updates)
    DBSession.flush()
    DBSession.commit()
    phenny.say("Points have been transferred from %s to %s" % (
        src_user.nick, dest_user.nick
    ))
transfer.rule = "^!transfer (.*) (.*)"
transfer.priority = 'medium'
transfer.thread = False


@smart_ignore
def give_respect(phenny, input):
    awarded_by = DBSession.query(User).filter(User.nick.ilike("%s%%" % input.nick)).first()
    words = input.split(" ")
    targets = []
    for identifier in ["++", "--"]:
        quanitity = 1
        if identifier == "--":
          quanitity = -1
        targets += [[(y, quanitity) for y in x.split(identifier) if y] for x in input.split(" ") if identifier in x]
    updates = []
    for target in set([x[0] for x in targets if any(x)]):
        if len(target[0]) >= 2 and not(target[0] == input.nick) or target[0] == phenny.nick:
            user_id = DBSession.query(User).filter(User.nick.ilike("%s%%" % target[0])).first()
            if not user_id:
                new_user = User()
                new_user.nick = target[0]
                DBSession.add(new_user)
                user_id = DBSession.query(User).filter(User.nick.ilike("%s%%" % target[0])).first()

            DBSession.add(Point("respect", user_id.id, awarded_by.id, target[1]))
            DBSession.flush()
            DBSession.commit()
            points = DBSession.query(Point).join(
                User, Point.user_id == User.id
            ).filter(
                Point.type == "respect"
            ).filter(User.nick.ilike("%s%%" % target[0])).all()
            user_points = 0
            for point in points:
                user_points += point.value
            updates.append("%s now has %d karma." % (user_id.nick, user_points))
    phenny.say(" ".join(updates))
give_respect.rule = r".*(\+\+|--)"
give_respect.priority = 'medium'
give_respect.thread = False


@smart_ignore
def trending(phenny, input):
    target = 4
    if input.groups()[0]:
        target = int(input.groups()[0])
        if target > 99:
            target = 99
        if target < 0:
            target = 0
    ignore_list = [
        "", "a", "about", "after", "all", "also", "am", "an", "and", "any",
        "are", "as", "at", "back", "be", "because", "been", "but", "by", "call",
        "can", "come", "could", "day", "did", "didn't", "do", "down", "each",
        "even", "find", "first", "for", "from", "get", "!give", "give", "go",
        "good", "!grab", "had", "has", "have", "he", "her", "him", "his", "how",
        "i", "if", "i'm", "in", "into", "is", "it", "it's", "its", "i've",
        "just", "know", "like", "lol", "long", "look", "made", "make", "many",
        "may", "me", "more", "most", "my", "new", "no", "!nocontext", "not",
        "now", "number", "of", "oh", "oil", "on", "one", "only", "or", "other",
        "our", "out", "over", "part", "people", "!points", "!quote", "!random",
        "said", "say", "see", "she", "should", "shouldn't", "so", "some",
        "take", "than", "that", "that's", "thats", "the", "their", "them",
        "then", "there", "these", "they", "think", "this", "time", "to",
        "!trending", "two", "up", "us", "use", "want", "was", "water", "way",
        "!wc", "we", "well", "were", "what", "when", "which", "who", "will",
        "with", "word", "work", "would", "write", "\x01action", "year", "you",
        "your", "you're",
    ]
    ignore_list += [phenny.nick.lower(),
                    "%s:" % phenny.nick.lower(),
                    "%s," % phenny.nick.lower()]
    ignore_list += [x.nick.lower() for x in DBSession.query(User).all()]
    ignore_list += ["%s:" % x.nick.lower() for x in DBSession.query(User).all()]
    ignore_list += ["%s," % x.nick.lower() for x in DBSession.query(User).all()]
    start_time = get_current_time() - datetime.timedelta(hours=target)
    words = [
        word for word in
        ' '.join([x.body for x in DBSession.query(Message).join(Room).filter(
            Room.name == input.sender
        ).filter(
            Message.created_at > start_time
        ).all()]).lower().split(' ') if word not in ignore_list
    ]

    most_common = collections.Counter(words).most_common(10)

    hours = "hours"
    if target == 1:
        hours = "hour"
    phenny.say(
        "Trending over last %d %s: %s " % (
            target,
            hours,
            ', '.join([
                "%s (%d)" % word for word in most_common
            ]),
        )
    )
trending.rule = r"^!trending\s?(\d+)?"
trending.priority = 'medium'
trending.thread = False


@smart_ignore
def unsad(phenny, input):
    phenny.say("%s*" % random.choice([
        ":)",
        ":-)",
        "(:",
        "(-:",
        ":D",
        ":-D",
        ":]",
        ":-]",
    ]))
unsad.rule = r'$^(:\W*[\(\[\{]|[D\)\]\}]\W*:)'
unsad.priority = 'medium'


@smart_ignore
def ignore(phenny, input):
    global ignored_nicks
    if not input.owner:
        return
    ignored_nicks.append(input.groups()[0])
    print ignored_nicks
ignore.rule = "^!ignore (.*)"
ignore.priority = 'medium'


@smart_ignore
def unignore(phenny, input):
    global ignored_nicks
    if not input.owner:
        return
    ignored_nicks.remove(input.groups()[0])
    print ignored_nicks
unignore.rule = "^!unignore (.*)"
unignore.priority = 'medium'


@smart_ignore
def op_giver(phenny, input):
    target = input.groups()[1]
    if input.owner:
        phenny.write(['MODE', "##brittslittlesliceofheaven", "+o", target])
op_giver.rule = r'^(!|\x01ACTION )op ([a-zA-Z0-9\-_]+)$'
op_giver.priority = 'medium'


@smart_ignore
def random_topic(phenny, input):
    target = input.groups()[1]

    if target.isdigit():
        quote = DBSession.query(Quote).filter(
            Quote.id == int(target)
        )
    else:
        quote = DBSession.query(Quote).join(
            Message
        ).join(User).join(Room).filter(
            Room.name == input.sender
        )
        if target:
            quote = quote.filter(Message.body.ilike("%%%s%%" % target))
    quote = quote.order_by(
        sa.func.random()
    ).first()
    if not quote:
        return
    topic = "Welcome to %s | <%s> %s" % (
        input.sender,
        quote.message.user.nick,
        quote.message.body
    )
    phenny.write(['TOPIC', input.sender], topic)
random_topic.rule = r'^(!)topic ?(.*)?$'
random_topic.priority = 'medium'
