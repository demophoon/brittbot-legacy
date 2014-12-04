#!/usr/bin/env python
'''
brittbot/autokick.py - jenni auto kick

More info:
 * jenni: https://github.com/myano/jenni/
'''

import re


def is_kick(jenni, channel, hostmask):
    for key, value in jenni.config.auto_kick_users.items():
        if channel not in value['rooms']:
            return

        usernick, username, userhost = hostmask

        kick = False
        kickmsg = key

        for rule in value['rules']:
            nick, user, host = rule['hostmask']
            matches = [
                re.match(re.compile(nick, re.IGNORECASE), usernick),
                re.match(re.compile(user, re.IGNORECASE), username),
                re.match(re.compile(host, re.IGNORECASE), userhost),
            ]
            if all(matches):
                kick = rule['kick']
                kickmsg = value['message']
        if kick:
            return (kick, kickmsg)
    return (kick, kickmsg)


def auto_kick(jenni, msg):
    hostmask = (msg.nick, msg.origin.user, msg.origin.host)
    kick, kickmsg = is_kick(jenni, msg.sender, hostmask)
    if msg.nick == jenni.bot.nick:
        return
    if kick:
        print "Kicking %s from %s for reason %s" % (
            msg.nick, msg.sender, kickmsg
        )
        jenni.write(['KICK', msg.sender, msg.nick, ":%s" % kickmsg])
    else:
        print "Joining %s: %s" % (
            msg.sender, msg.nick
        )
auto_kick.event = 'JOIN'
auto_kick.rule = '.*'
auto_kick.priority = 'high'


def nametrigger(jenni, input):
    names = re.split(' ', input)
    #names = [n.split('!')[0] for n in names]
    #names = [n.replace('~', '') for n in names]
    print names
    print input.sender
nametrigger.event = '353'
nametrigger.rule = '(.*)'
nametrigger.priority = 'high'
