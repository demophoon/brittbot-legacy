#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/markov.py - Markov string generator

import random
from textblob import TextBlob
from modules.brittbot.model import Message


def markov_generator(jenni, msg):
    args = msg.groups()[1]
    target = None
    starting_word = None
    room = msg.sender
    if room == 'demophoon':
        room = '#internship'
    if args:
        args = args.split(" ")
        if len(args) >= 1:
            target = args[0]
        if len(args) >= 2:
            starting_word = args[1]
    query = jenni.db.query(Message.body).filter(
        Message.room == room,
    )
    if target and not target.lower() == 'everything':
        target = target.strip()
        query = query.filter(Message.nick == target)
    msgs = query.order_by(
        Message.created_at.desc()
    ).limit(5000).all()
    if not msgs:
        return
    msgs = [x[0] for x in msgs]
    t = {}
    for line in msgs:
        try:
            ngrams = TextBlob(" ".join(line.split(" ")[2:])).ngrams(n=5)
        except Exception:
            pass
        for ngram in ngrams:
            grams = list(ngram)
            word = ','.join(grams[0:2])
            if word not in t:
                t[word] = []
            t[word].append(grams[2:])
    for _ in range(2):
        if not starting_word:
            for _ in range(5):
                starting_word = random.choice(t.keys()).split(',')
                tags = TextBlob(starting_word[0].split(",")[0]).pos_tags
                print tags
                if tags[0][1] in ['VB', 'NN', 'JJ', 'PRP']:
                    break
        else:
            starting_choices = [x for x in t.keys() if starting_word in x]
            if starting_choices:
                starting_word = random.choice(starting_choices).split(',')
        reply = starting_word
        for jumps in range(random.randint(10,24)):
            words = t.get(','.join(reply[-2:]))
            print "{}".format(' '.join(reply))
            if not words:
                if jumps >= 3:
                    break
                if len(reply) < 2:
                    break
                tags = TextBlob(reply[-1]).pos_tags
                if tags[0][1] in ['VB', 'NN', 'PRP']:
                    break
                print "removing {}".format(reply[-1])
                reply = reply[:-1]
                continue
            words = random.choice(words)
            reply += words
        if jumps >= 3:
            break
    if len(reply) <= 1:
        reply = "That didn't come up with anything interesting. Try one of these words instead: "
        reply += ', '.join([random.choice(t.keys()) for _ in range(3)])
        jenni.reply(reply)
        return
    reply = ' '.join(reply)
    jenni.say(reply)
markov_generator.commands = ['markov']
