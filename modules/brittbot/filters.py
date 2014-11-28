#!/usr/bin/env python
'''
brittbot/filters.py - jenni Spam filters

More info:
 * jenni: https://github.com/myano/jenni/
'''

import re

ignored_nicks = [
    ".*bot",
]

limited_channels = {
}


def check_ignore(msg):
    ignore = False
    if not msg.sender.startswith("#"):
        ignore = True
    for ignored_nick in ignored_nicks:
        if re.search(re.compile(ignored_nick, re.IGNORECASE), msg.nick):
            ignore = True
            print "%s is ignored by rule %s" % (
                msg.nick,
                ignored_nick
            )
    if msg.admin:
        ignore = False
    return ignore


def smart_ignore(fn):
    def callable(jenni, msg):
        print fn.__name__
        if check_ignore(msg):
            return None
        if msg.sender in limited_channels:
            if limited_channels[msg.sender].get('allowed'):
                if fn in [x._original for x in limited_channels[msg.sender]['allowed']]:
                    return fn
                return None
            if fn in [x._original for x in limited_channels[msg.sender]['ignored']]:
                return None
        return fn(jenni, msg)
    callable._original = fn
    return callable
