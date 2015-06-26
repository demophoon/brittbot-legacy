#!/usr/bin/env python
'''
brittbot/autokick.py - jenni auto kick

More info:
 * jenni: https://github.com/myano/jenni/
'''

import re

allowed_rooms = [
    '##brittslittlesliceofheaven',
    '##brittbot',
]


def init_kick_brain(jenni):
    brain = jenni.brain
    if 'kicks' not in brain:
        brain['kicks'] = {}
        jenni.save_brain()


def is_kick(jenni, channel, hostmask):
    kick = False
    kickmsg = None
    for key, value in jenni.config.auto_kick_users.items():
        if channel not in value['rooms'] and channel not in allowed_rooms:
            return (False, "")

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
    init_kick_brain(jenni)
    hostmask = (msg.nick, msg.origin.user, msg.origin.host)
    kick, kickmsg = is_kick(jenni, msg.sender, hostmask)
    if msg.sender not in jenni.online_users:
        jenni.online_users[msg.sender] = []
    jenni.online_users[msg.sender] += [msg.nick]
    if msg.nick == jenni.nick:
        return
    if kick:
        if msg.nick not in jenni.brain['kicks']:
            jenni.brain['kicks'][msg.nick] = 0
        jenni.brain['kicks'][msg.nick] += 1
        if jenni.brain['kicks'][msg.nick] > 3:
            jenni.write(['MODE', msg.sender, "+b", "%s!%s@%s" % hostmask])
        jenni.save_brain()
        print "Kicking %s from %s for reason %s" % (
            msg.nick, msg.sender, kickmsg
        )
        jenni.write(['KICK', msg.sender, msg.nick, ":%s" % kickmsg])
        jenni.brain['kicks']
    else:
        print "Joining %s: %s" % (
            msg.sender, msg.nick
        )
auto_kick.event = 'JOIN'
auto_kick.rule = '.*'
auto_kick.priority = 'high'


def user_part(jenni, msg):
    if msg.sender in jenni.online_users:
        if msg.nick in jenni.online_users[msg.sender]:
            jenni.online_users[msg.sender].remove(msg.nick)
    else:
        jenni.online_users[msg.sender] = []
user_part.event = 'PART'
user_part.rule = '.*'
user_part.priority = 'high'


def user_quit(jenni, msg):
    if msg.sender in jenni.online_users:
        if msg.nick in jenni.online_users[msg.sender]:
            jenni.online_users[msg.sender].remove(msg.nick)
    else:
        jenni.online_users[msg.sender] = []
user_quit.event = 'QUIT'
user_quit.rule = '.*'
user_quit.priority = 'high'


def nametrigger(jenni, input):
    channel = input.args[2]
    names = re.split(' ', input)
    if channel not in jenni.online_users:
        jenni.online_users[channel] = []
    jenni.online_users[channel] += names
nametrigger.event = '353'
nametrigger.rule = '(.*)'
nametrigger.priority = 'high'


def mean_kick(jenni, msg):
    reply = "%s you too %s" % (
        msg.groups()[0],
        msg.nick
    )
    if msg.sender in allowed_rooms:
        jenni.write(['KICK', msg.sender, msg.nick, ":%s" % reply])
    jenni.say(reply)
mean_kick.rule = '(?i)(screw|fuck|i hate)(?: you)? $nickname'
mean_kick.priority = 'high'
