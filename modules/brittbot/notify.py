#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/notify.py - Subscribe and notify to lists


def setup_brain(jenni, msg):
    if 'ping' not in jenni.brain:
        jenni.brain['ping'] = {}
    if msg.sender not in jenni.brain['ping']:
        jenni.brain['ping'][msg.sender] = {}


def subscribe_to_ping(jenni, msg):
    setup_brain(jenni, msg)
    topic = msg.groups()[0].strip()
    normalized_topic = topic.lower()
    if normalized_topic not in jenni.brain['ping'][msg.sender]:
        jenni.brain['ping'][msg.sender][normalized_topic] = []
    jenni.brain['ping'][msg.sender][normalized_topic].append(msg.nick)
    jenni.brain['ping'][msg.sender][normalized_topic] = list(set(jenni.brain['ping'][msg.sender][normalized_topic]))
    jenni.brain.save()
    jenni.reply('You have been subscribed to {} pings'.format(topic))
subscribe_to_ping.rule = r'^!subscribe (.*)$'


def unsubscribe_to_ping(jenni, msg):
    setup_brain(jenni, msg)
    topic = msg.groups()[0].strip()
    normalized_topic = topic.lower()
    if normalized_topic not in jenni.brain['ping'][msg.sender]:
        jenni.brain['ping'][msg.sender][normalized_topic] = []
    if msg.nick not in jenni.brain['ping'][msg.sender][normalized_topic]:
        jenni.reply("You are not currently subscribed to {}.".format(normalized_topic))
        return
    jenni.brain['ping'][msg.sender][normalized_topic].remove(msg.nick)
    jenni.brain.save()
    jenni.reply('You have been unsubscribed to {} pings'.format(topic))
unsubscribe_to_ping.rule = r'^!unsubscribe (.*)$'


def ping_users(jenni, msg):
    import random
    from modules.brittbot.helpers import (colors, colorize)
    setup_brain(jenni, msg)
    topic = msg.groups()[0].strip()
    normalized_topic = topic.lower()
    if normalized_topic not in jenni.brain['ping'][msg.sender]:
        jenni.reply('Invalid topic')
        return
    jenni.brain['ping'][msg.sender][normalized_topic] = list(set(jenni.brain['ping'][msg.sender][normalized_topic]))
    pings = ', '.join(jenni.brain['ping'][msg.sender][normalized_topic])
    replies = [
        "IT IS TIME FOR {topic}, ",
        "{topic}?",
        "You all have been summoned for {topic}.",
        "Join me on a quest for {topic}.",
        "{topic}! {topic}! {topic}!",
        "I cannot hear you over the sound of my {topic}.",
        "Ring ring! {topic} is calling!",
        "Anybody want some {topic}?",
        "TACO BELL! uh.. I mean {topic}...",
        "May the {topic} be with you.",
        "Show me the {topic}.",
        "Needs more {topic}.",
        "You can't handle the {topic}!",
        "We're gonna need a bigger {topic}.",
        "BEEP BOOP {topic}!",
        "I feel the need, the need for {topic}!",
    ]
    reply = random.choice(replies) + " {users}"
    jenni.say(reply.format(topic=colorize(topic, fg=colors['cyan']), users=pings))
ping_users.rule = r'^!ping (.*)$'
