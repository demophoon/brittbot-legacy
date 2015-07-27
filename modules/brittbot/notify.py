#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/notify.py - Subscribe and notify to lists

from modules.brittbot.filters import smart_ignore


def setup_brain(jenni, msg):
    if 'ping' not in jenni.brain:
        jenni.brain['ping'] = {}
    if msg.sender not in jenni.brain['ping']:
        jenni.brain['ping'][msg.sender] = {}


@smart_ignore
def subscribe_to_ping(jenni, msg):
    setup_brain(jenni, msg)
    topic = msg.groups()[0].strip()
    if topic not in jenni.brain['ping'][msg.sender]:
        jenni.brain['ping'][msg.sender][topic] = []
    jenni.brain['ping'][msg.sender][topic].append(msg.nick)
    jenni.brain.save()
    jenni.reply('You have been subscribed to {} pings'.format(topic))
subscribe_to_ping.rule = r'^!subscribe (.*)$'


@smart_ignore
def unsubscribe_to_ping(jenni, msg):
    setup_brain(jenni, msg)
    topic = msg.groups()[0].strip()
    if topic not in jenni.brain['ping'][msg.sender]:
        jenni.brain['ping'][msg.sender][topic] = []
    if msg.nick not in jenni.brain['ping'][msg.sender][topic]:
        jenni.reply("You are not currently subscribed to {}.".format(topic))
        return
    jenni.brain['ping'][msg.sender][topic].remove(msg.nick)
    jenni.brain.save()
    jenni.reply('You have been unsubscribed to {} pings'.format(topic))
unsubscribe_to_ping.rule = r'^!unsubscribe (.*)$'


@smart_ignore
def ping_users(jenni, msg):
    setup_brain(jenni, msg)
    topic = msg.groups()[0].strip()
    if topic not in jenni.brain['ping'][msg.sender]:
        jenni.reply('Invalid topic')
        return
    pings = ', '.join(jenni.brain['ping'][msg.sender][topic])
    jenni.reply('Ping for {}: {}'.format(topic, pings))
ping_users.rule = r'^!ping (.*)$'
