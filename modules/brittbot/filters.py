#!/usr/bin/env python
'''
brittbot/filters.py - jenni Spam filters

More info:
 * jenni: https://github.com/myano/jenni/
'''

import re
from functools import wraps

limited_channels = {
}


def is_allowed(function_name, jenni, msg):
    ignored_nicks = jenni.brain['filtered_nicks']
    irc_room = msg.sender
    if 'filters' not in jenni.brain:
        jenni.brain['filters'] = jenni.config.channel_filters
        jenni.save_brain()
    filters = jenni.brain["filters"]
    allowed = True
    if not irc_room.startswith("#") and not msg.admin:
        allowed = False
    for nick in ignored_nicks:
        if re.search(re.compile(nick, re.IGNORECASE), msg.nick):
            allowed = False
    if msg.nick in jenni.brain['approval']:
        if jenni.brain['approval'][msg.nick] < -5:
            allowed = False
            msg.friend = False
            msg.enemy = True
        elif jenni.brain['approval'][msg.nick] > 5:
            msg.friend = True
            msg.enemy = False
    if msg.admin:
        allowed = True
    if irc_room in filters:
        if 'blocked' in filters[irc_room]:
            if function_name in filters[irc_room]['blocked']:
                allowed = False
        if 'allowed' in filters[irc_room]:
            allowed = function_name in filters[irc_room]['allowed']
    return allowed


def smart_ignore(fn):
    @wraps(fn)
    def callable(jenni, msg):
        function_name = fn.__name__
        default_fn = lambda jenni, msg: None
        if not is_allowed(function_name, jenni, msg):
            return default_fn
        return fn(jenni, msg)
    return callable


def modify_filtered(jenni, msg):
    if not msg.admin:
        return
    action, room, function = msg.groups()
    if room not in jenni.brain['filters']:
        jenni.brain['filters'][room] = {}
    if 'blocked' not in jenni.brain['filters'][room]:
        jenni.brain['filters'][room]['blocked'] = []
    if action == 'enable':
        jenni.brain['filters'][room]['blocked'].remove(function)
    else:
        jenni.brain['filters'][room]['blocked'].append(function)
    jenni.save_brain()
    jenni.reply('Function `%s` has been %sd in `%s`' % (
        function, action, room
    ))
modify_filtered.rule = '!(enable|disable) (\S+) (.+)'


def modify_ignored(jenni, msg):
    if not msg.admin:
        return
    action, nick = msg.groups()
    if 'filtered_nicks' not in jenni.brain:
        jenni.brain['filtered_nicks'] = []
    if action == 'unignore':
        jenni.brain['filtered_nicks'].remove(nick)
    else:
        jenni.brain['filtered_nicks'].append(nick)
    jenni.save_brain()
    jenni.reply('`%s` has been %sd' % (
        nick, action
    ))
modify_ignored.rule = '!(ignore|unignore) (\S+)'
