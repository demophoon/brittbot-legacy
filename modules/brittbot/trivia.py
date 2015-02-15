#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/trivia.py - Trivia bot!

import time
import re
import urllib
import json
import random

from modules.brittbot.filters import smart_ignore
from modules.brittbot.helpers import colorize, colors

trivia_room = '##brittbot-jeopardy'
trivia_rooms = [trivia_room]


def init_trivia_brain(jenni):
    brain = jenni.brain
    if 'trivia' not in brain:
        brain['trivia'] = {
            'users': {},
            'rooms': {},
        }
    jenni.save_brain()


def init_user_brain(jenni, nick):
    if nick not in jenni.brain['trivia']['users']:
        jenni.brain['trivia']['users'][nick] = {
            'correct': 0,
            'incorrect': 0,
            'skipped': 0,
            'banned': 0,
        }
    if not 'banned' in jenni.brain['trivia']['users'][nick]:
        jenni.brain['trivia']['users'][nick]['banned'] = 0
    jenni.save_brain()


@smart_ignore
def trivia(jenni, msg):
    hostmask = (msg.nick, msg.origin.user, msg.origin.host)
    init_trivia_brain(jenni)
    chan = msg.sender
    if chan not in trivia_rooms:
        if trivia_room not in jenni.channels:
            jenni.write(['JOIN', trivia_room])
            time.sleep(.5)
            jenni.write(['MODE', trivia_room, "+i"])
            jenni.channels.append(trivia_room)
        jenni.msg(msg.nick, "Join %s" % (
            trivia_room
        ))
        jenni.write(['INVITE', msg.nick, trivia_room])
        return
    rooms = jenni.brain['trivia']['rooms']
    if chan not in rooms:
        rooms[chan] = {
            'category': None,
            'question': None,
            'answer': None,
            'attempts': 0,
            'noplay': [],
            'noplay_hostmask': [],
        }
    points = None
    if not rooms[chan]['question']:
        while not rooms[chan]['question']:
            count = 1
            if chan != trivia_room:
                count = 25
            questions = json.loads(
                urllib.urlopen("http://jservice.io/api/random?count=%s" % (count, )).read())
            for question in questions:
                if not question['value']:
                    continue
                if not points:
                    points = int(question['value'])
                current_points = int(question['value'])
                if chan != trivia_room:
                    current_points *= float(len(question['question']))
                    current_points += len(question['answer'].split(' '))
                    current_points /= len(question['answer'])
                if current_points >= points:
                    points = current_points
                    rooms[chan]['category'] = question['category']['title']
                    rooms[chan]['question'] = question['question']
                    rooms[chan]['answer'] = question['answer']
                    rooms[chan]['attempts'] = 1
        rooms[chan]['noplay'] = []
        rooms[chan]['noplay_hostmask'] = []
    if not points:
        points = 1000
    print "%s points" % (points, )
    rooms[chan]['answer'] = rooms[chan]['answer'].replace("<i>", "")
    rooms[chan]['answer'] = rooms[chan]['answer'].replace("</i>", "")
    rooms[chan]['answer'] = rooms[chan]['answer'].replace("\"", "")
    reply = "The category is \"%s\". %s" % (
        colorize(rooms[chan]['category'], fg=colors['orange']),
        colorize(rooms[chan]['question'], fg=colors['orange']),
    )
    jenni.write(['NOTICE', msg.sender, ":%s" % reply])
    jenni.save_brain()
trivia.rule = r"^($nickname\W |!)trivia$"


@smart_ignore
def trivia_answer(jenni, msg):
    hostmask = (msg.nick, msg.origin.user, msg.origin.host)
    chan = msg.sender
    if chan not in trivia_rooms:
        return
    rooms = jenni.brain['trivia']['rooms']
    init_user_brain(jenni, msg.nick)

    if chan not in rooms:
        return
    if not rooms[chan]['question']:
        return
    ignored_words = [
        'the',
        'i',
        'a',
        'an',
        'accepted',
        'or',
        'he',
        'his',
        'her',
        'hers',
    ]
    pattern = re.compile("[\W]+")

    if jenni.brain['trivia']['users'][msg.nick]['banned'] > 1:
        return
    guess = msg.groups()[0].lower()
    guess = [pattern.sub('', y) for y in guess.split(" ")]
    guess = [x for x in guess if x]
    guess += [x[:-1] for x in guess if x.endswith("s")]
    guess += [x + "s" for x in guess if not x.endswith("s")]
    answer = rooms[chan]['answer'].lower()
    answer = [pattern.sub('', y)
              for y in answer.split(" ") if y not in ignored_words]
    correct = float(sum([x in answer for x in guess]))
    correct = max(correct, float(sum([x in ''.join(answer) for x in guess])))

    drop_lol = ['drop', 'table', 'answers']
    if all([x in drop_lol for x in guess]) and msg.admin:
        reply = "Shutting down."
        jenni.write(['NOTICE', msg.sender, ":%s" % reply])
        exit()
        return

    correctness_threshold = .5

    if correct/len(answer) >= correctness_threshold:
        if msg.nick in rooms[chan]['noplay']:
            jenni.reply("Thanks for ruining the game."
                        " Yes. The answer is \"%s\" but you "
                        "cheated to find out. This is your last warning." %
                        (rooms[chan]['answer']))
            jenni.brain['trivia']['users'][msg.nick]['banned'] += 1
            if jenni.brain['trivia']['users'][msg.nick]['banned'] > 1:
                kickmsg = "No cheating allowed. Contact `demophoon` to be forgiven"
                jenni.write(['MODE', msg.sender, "+b", "%s!%s@%s" % hostmask])
                jenni.write(['KICK', msg.sender, msg.nick, ":%s" % kickmsg])
            rooms[chan]['question'] = None
        else:
            jenni.reply("You are %s! The answer is %s. W/L %d/%d" % (
                colorize("correct", fg=colors['green']),
                rooms[chan]['answer'],
                jenni.brain['trivia']['users'][msg.nick]['correct'],
                jenni.brain['trivia']['users'][msg.nick]['incorrect'],
            ))
            rooms[chan]['question'] = None
            jenni.brain['trivia']['users'][msg.nick]['correct'] += 1
    elif rooms[chan]['attempts'] <= 0:
        jenni.reply("You are %s. The correct answer is %s" % (
            colorize("incorrect", fg=colors['red']),
            rooms[chan]['answer']
        ))
        jenni.brain['trivia']['users'][msg.nick]['incorrect'] += 1
        rooms[chan]['question'] = None
    else:
        jenni.reply("You are %s. %s more attempts" % (
            colorize("incorrect", fg=colors['red']),
            rooms[chan]['attempts']
        ))
        jenni.brain['trivia']['users'][msg.nick]['incorrect'] += 1
        rooms[chan]['attempts'] -= 1
        #if msg.nick == 'quakeaddict':
        #    reply = "Wow. That was wrong. Just leave. You are awarded no points. May god have mercy on your soul."
        #    jenni.write(['KICK', msg.sender, msg.nick, ":%s" % reply])
    if msg.sender in trivia_rooms and rooms[chan]['question'] == None:
        trivia(jenni, msg)
    jenni.save_brain()
trivia_answer.rule = r"^(?:$nickname\W? )?(?:w?W?hat|w?W?ho) \w+ (.*)\??"


@smart_ignore
def trivia_giveup(jenni, msg):
    hostmask = (msg.nick, msg.origin.user, msg.origin.host)
    chan = msg.sender
    if chan not in trivia_rooms:
        return
    rooms = jenni.brain['trivia']['rooms']
    init_user_brain(jenni, msg.nick)
    jenni.brain['trivia']['users'][msg.nick]['skipped'] += 1
    if jenni.brain['trivia']['users'][msg.nick]['banned'] > 1:
        return
    jenni.brain['trivia']['rooms'][chan]['noplay'].append(msg.nick)
    if chan not in rooms:
        return
    if not rooms[chan]['question']:
        return
    jenni.msg(msg.nick, "The correct answer is %s" % (
        rooms[chan]['answer']
    ))
    hostmask = "%s!%s@%s" % hostmask
    #jenni.write(['MODE', msg.sender, "+q", hostmask])
    jenni.brain['trivia']['rooms'][chan]['noplay_hostmask'].append(hostmask)
    jenni.save_brain()
trivia_giveup.rule = r"^$nickname\W? i (give up|have no idea|don'?t know)"


@smart_ignore
def trivia_forgive(jenni, msg):
    if not msg.admin:
        return
    init_user_brain(jenni, msg.nick)
    nick = msg.groups()[0]
    if nick == 'me':
        nick = msg.nick
    jenni.brain['trivia']['users'][nick]['banned'] = 0
    jenni.reply("I have forgiven %s for you. "
                "You might need to unban them from any rooms I am in." % (
                    nick
                ))
    jenni.save_brain()
trivia_forgive.rule = r"^$nickname\W? forgive (.*)"


@smart_ignore
def trivia_skip(jenni, msg):
    chan = msg.sender
    if chan not in trivia_rooms:
        return
    rooms = jenni.brain['trivia']['rooms']
    if rooms[chan]['attempts'] > 5:
        jenni.reply("Nou.")
        return
    init_user_brain(jenni, msg.nick)
    jenni.reply("Skipping question.")
    jenni.brain['trivia']['users'][msg.nick]['skipped'] += 1
    rooms[chan]['question'] = None
    trivia(jenni, msg)
trivia_skip.rule = r"$nickname\W? skip"


@smart_ignore
def trivia_points(jenni, msg):
    chan = msg.sender
    nick = msg.nick
    if msg.groups()[0]:
        nick = msg.groups()[0].strip()
    init_user_brain(jenni, nick)
    user = jenni.brain['trivia']['users'][nick]
    corrects = 's'
    incorrects = 's'
    skips = 's'
    if user['correct'] == 1:
        corrects = ''
    if user['incorrect'] == 1:
        incorrects = ''
    if user['skipped'] == 1:
        skips = ''
    if nick == msg.nick:
        reply = "You have"
    else:
        reply = "%s has" % nick

    reply += " answered %d question%s correctly," % (
        user['correct'],
        corrects,
    )
    reply += " gave %d incorrect answer%s," % (
        user['incorrect'],
        incorrects,
    )
    reply += " and skipped %d question%s." % (
        user['skipped'],
        skips,
    )
    jenni.reply(reply)
trivia_points.rule = r"^!triviapoints( .*)?"


def join_trivia_handle(jenni, msg):
    chan = msg.sender
    if chan != trivia_room:
        return
    if msg.admin:
        jenni.write(['MODE', msg.sender, "+o", msg.nick])
    trivia(jenni, msg)
    init_user_brain(jenni, msg.nick)
join_trivia_handle.event = 'JOIN'
join_trivia_handle.rule = '.*'
join_trivia_handle.priority = 'high'


def shutdown_handler(jenni, msg):
    hostmask = ('*', '*', '*')
    if not msg.owner:
        return
    reply = "Shutting down."
    for room in trivia_rooms:
        jenni.write(['NOTICE', room, ":%s" % reply])
        time.sleep(1)
    jenni.write(['MODE', trivia_room, "-i"])
    print "Powering off trivia."
shutdown_handler.rule = '$^'
