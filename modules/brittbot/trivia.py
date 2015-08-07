#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/trivia.py - Trivia bot!

import random
import time
import re
import urllib
import json

from modules.brittbot.filters import smart_ignore
from modules.brittbot.helpers import colorize, colors

trivia_room = '##brittbot-trivia'
trivia_rooms = [trivia_room, '#brittbot-trivia']
cached_questions = []
last_question_asked = 0


def init_trivia_brain(jenni):
    brain = jenni.brain
    if 'trivia' not in brain:
        brain['trivia'] = {
            'users': {},
            'rooms': {},
        }
    jenni.brain.save()


def init_user_brain(jenni, nick):
    if nick not in jenni.brain['trivia']['users']:
        jenni.brain['trivia']['users'][nick] = {
            'correct': 0,
            'incorrect': 0,
            'skipped': 0,
            'banned': 0,
        }
    if 'banned' not in jenni.brain['trivia']['users'][nick]:
        jenni.brain['trivia']['users'][nick]['banned'] = 0
    jenni.brain.save()


@smart_ignore
def trivia_hint(jenni, msg):
    global last_question_asked
    if time.time() - last_question_asked < 2:
        return
    import string
    hint_chars = string.letters + string.digits
    chan = msg.sender
    rooms = jenni.brain['trivia']['rooms']
    if chan not in rooms:
        return
    answer = rooms[chan]['answer'].lower()
    answer = answer.replace('\\', "")
    if not len(rooms[chan]['hint']) > 5:
        all_letters = [x for x in list(set(answer)) if x not in rooms[chan]['hint']]
        all_letters = [x for x in all_letters if x in hint_chars]
        rooms[chan]['hint'].append(random.choice(all_letters))
    hint_str = map(lambda l: l if l in rooms[chan]['hint'] or l not in hint_chars else "_", answer)
    hint_str = " ".join(hint_str)
    jenni.reply(hint_str)
trivia_hint.rule = "^!hint$"


@smart_ignore
def trivia(jenni, msg):
    global cached_questions
    global last_question_asked
    init_trivia_brain(jenni)
    chan = msg.sender
    if chan not in trivia_rooms:
        if trivia_room not in jenni.channels:
            jenni.write(['JOIN', trivia_room])
            time.sleep(.5)
            jenni.write(['MODE', trivia_room, "+i"])
            jenni.channels.append(trivia_room)
        jenni.reply("Join %s" % (trivia_room))
        jenni.write(['INVITE', msg.nick, trivia_room])
        return
    rooms = jenni.brain['trivia']['rooms']
    if chan not in rooms:
        rooms[chan] = {
            'category': None,
            'question': None,
            'answer': None,
            'hint': [],
            'attempts': 0,
            'noplay': [],
            'noplay_hostmask': [],
        }
    points = None
    if not rooms[chan]['question']:
        while len(cached_questions) <= 1:
            count = 50
            questions = json.loads(
                urllib.urlopen("http://jservice.io/api/random?count=%s" % (count, )).read())
            for question in questions:
                if not question['value']:
                    continue
                if "http" in question['answer']:
                    continue
                cached_questions.append(question)
    if not rooms[chan]['question']:
        last_question_asked = time.time()
        question = cached_questions.pop()
        rooms[chan]['category'] = question['category']['title']
        rooms[chan]['question'] = question['question']
        rooms[chan]['answer'] = question['answer']
        rooms[chan]['attempts'] = 1
        rooms[chan]['hint'] = []
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
    jenni.write(['PRIVMSG', msg.sender, ":%s" % reply])
    jenni.brain.save()
trivia.rule = r"^($nickname\W |!)trivia$"


@smart_ignore
def trivia_answer(jenni, msg):
    global last_question_asked
    if time.time() - last_question_asked < 2:
        return
    import string
    hint_chars = string.letters + string.digits
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
        'and',
    ]
    pattern = re.compile("[\W]+")

    if jenni.brain['trivia']['users'][msg.nick]['banned'] > 1:
        return
    guess = msg.groups()[0].lower()
    guess = ''.join(x for x in guess if x in hint_chars)
    guess = [pattern.sub('', y) for y in guess.split(" ") if y not in ignored_words]
    guess = [x for x in guess if x]
    guess += [x[:-1] for x in guess if x.endswith("s")]
    guess += [x + "s" for x in guess if not x.endswith("s")]
    answer = rooms[chan]['answer'].lower()
    answer = ''.join(x for x in answer if x in hint_chars)
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

    if correct / len(answer) >= correctness_threshold:
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
    if msg.sender in trivia_rooms and not rooms[chan]['question']:
        trivia(jenni, msg)
    jenni.brain.save()
trivia_answer.rule = r"^(?:$nickname\W? )?(?:w?W?hat|w?W?ho) \w+ (.*)\??"


@smart_ignore
def trivia_giveup(jenni, msg):
    global last_question_asked
    if time.time() - last_question_asked < 2:
        return
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
    jenni.brain['trivia']['rooms'][chan]['noplay_hostmask'].append(hostmask)
    jenni.brain.save()
trivia_giveup.rule = r"^(?:$nickname\W? i (?:give up|have no idea|don'?t know).*|!giveup)$"


@smart_ignore
def trivia_forgive(jenni, msg):
    init_user_brain(jenni, msg.nick)
    nick = msg.groups()[0]
    if nick == 'me':
        nick = msg.nick
    if nick == msg.nick and not msg.owner:
        return
    jenni.brain['trivia']['users'][nick]['banned'] = 0
    jenni.reply("I have forgiven %s for you. "
                "You might need to unban them from any rooms I am in." % (
                    nick
                ))
    jenni.brain.save()
trivia_forgive.rule = r"^$nickname\W? forgive (.*)"


@smart_ignore
def trivia_skip(jenni, msg):
    global last_question_asked
    if time.time() - last_question_asked < 2:
        return
    chan = msg.sender
    if chan not in trivia_rooms:
        return
    rooms = jenni.brain['trivia']['rooms']
    if rooms[chan]['attempts'] > 5:
        jenni.reply("Nou.")
        return
    init_user_brain(jenni, msg.nick)
    #jenni.reply("Skipping question.")
    jenni.brain['trivia']['users'][msg.nick]['skipped'] += 1
    rooms[chan]['question'] = None
    trivia(jenni, msg)
trivia_skip.rule = r"^($nickname\W? skip|!skip)$"


@smart_ignore
def trivia_points(jenni, msg):
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
    if not msg.owner:
        return
    reply = "Shutting down."
    for room in trivia_rooms:
        jenni.write(['NOTICE', room, ":%s" % reply])
        time.sleep(1)
    jenni.write(['MODE', trivia_room, "-i"])
    print "Powering off trivia."
shutdown_handler.rule = '$^'
