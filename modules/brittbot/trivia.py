#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/trivia.py - Trivia bot!

import re
import urllib
import json

from modules.brittbot.filters import smart_ignore


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
        }
    jenni.save_brain()


@smart_ignore
def trivia(jenni, msg):
    init_trivia_brain(jenni)
    chan = msg.sender
    rooms = jenni.brain['trivia']['rooms']
    if chan not in rooms:
        rooms[chan] = {
            'category': None,
            'question': None,
            'answer': None,
            'attempts': 0,
        }
    if not rooms[chan]['question']:
        while not rooms[chan]['question']:
            question = json.loads(
                urllib.urlopen("http://jservice.io/api/random").read())[0]
            rooms[chan]['category'] = question['category']['title']
            rooms[chan]['question'] = question['question']
            rooms[chan]['answer'] = question['answer']
            rooms[chan]['attempts'] = 2
    jenni.say("The category is \"%s\". %s" % (
        rooms[chan]['category'],
        rooms[chan]['question'],
    ))
    jenni.save_brain()
trivia.rule = r"^($nickname\W |!)trivia$"


@smart_ignore
def trivia_answer(jenni, msg):
    chan = msg.sender
    rooms = jenni.brain['trivia']['rooms']
    init_user_brain(jenni, msg.nick)

    if chan not in rooms:
        return
    if not rooms[chan]['question']:
        return
    ignored_words = ['the', 'i', 'a', 'or', 'he', 'his', 'her', 'hers']
    pattern = re.compile("[\W]+")
    guess = msg.groups()[0].lower()
    guess = [pattern.sub('', y) for y in guess.split(" ")]
    answer = rooms[chan]['answer'].lower()
    answer = [pattern.sub('', y)
              for y in answer.split(" ") if y not in ignored_words]
    correct = float(sum([x in answer for x in guess]))
    if correct/len(answer) >= .5:
        jenni.reply("You are correct! %s" % rooms[chan]['answer'])
        rooms[chan]['question'] = None
        jenni.brain['trivia']['users'][msg.nick]['correct'] += 1
    elif rooms[chan]['attempts'] <= 0:
        jenni.reply("Incorrect answer. The correct answer is %s" % (
            rooms[chan]['answer']
        ))
        jenni.brain['trivia']['users'][msg.nick]['incorrect'] += 1
        rooms[chan]['question'] = None
    else:
        jenni.reply("Incorrect answer. %s more attempts" % (
            rooms[chan]['attempts']
        ))
        jenni.brain['trivia']['users'][msg.nick]['incorrect'] += 1
        rooms[chan]['attempts'] -= 1
    jenni.save_brain()
trivia_answer.rule = r"^$nickname\W? (?:what|who) \w+ (.*)\??"


@smart_ignore
def trivia_giveup(jenni, msg):
    chan = msg.sender
    rooms = jenni.brain['trivia']['rooms']
    init_user_brain(jenni, msg.nick)
    jenni.brain['trivia']['users'][msg.nick]['skipped'] += 1
    if chan not in rooms:
        return
    if not rooms[chan]['question']:
        return

    jenni.reply("The correct answer is %s" % (
        rooms[chan]['answer']
    ))
    rooms[chan]['question'] = None
    jenni.save_brain()
trivia_giveup.rule = r"^$nickname\W? i (give up|have no idea|don'?t know)"


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
