#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/helpers.py - Various methods for formatting messages

from __future__ import unicode_literals
import sys
import datetime
import random

if sys.version_info.major >= 3:
    unicode = str

CONTROL_NORMAL = u'\x0f'
CONTROL_COLOR = u'\x03'
CONTROL_UNDERLINE = u'\x1f'
CONTROL_BOLD = u'\x02'

colors = {
    'white': '00',
    'black': '01',
    'blue': '02',
    'navy': '02',
    'green': '03',
    'red': '04',
    'brown': '05',
    'maroon': '05',
    'purple': '06',
    'orange': '07',
    'olive': '07',
    'yellow': '08',
    'light green': '09',
    'lime': '09',
    'teal': '10',
    'light cyan': '11',
    'cyan': '11',
    'aqua': '11',
    'light blue': '12',
    'royal': '12',
    'pink': '13',
    'light purple': '13',
    'fuchsia': '13',
    'grey': '14',
    'light grey': '15',
    'silver': '15',
}


def color_test(jenni, msg):
    if not msg.admin:
        return
    reply = []
    for color in colors:
        reply.append(colorize(colors[color], color))
    reply = u' '.join(reply)
    print repr(reply)
    jenni.reply(reply)
color_test.rule = r"^color$"


def action(msg):
    msg = '\x01ACTION %s\x01' % msg
    return msg


def colorize(msg, fg=None, bg=None):
    if not fg and not bg:
        final = msg
    elif bg:
        final = ''.join([CONTROL_COLOR, fg, ',', bg, msg, CONTROL_COLOR])
    else:
        final = ''.join([CONTROL_COLOR, fg, msg, CONTROL_COLOR])
    return final


def colorize_msg(msg):
    final = unicode()
    rainbow = [
        'red',
        'orange',
        'yellow',
        'green',
        'cyan',
        'blue',
        'purple',
    ]
    starting_index = random.choice(range(len(rainbow)))
    for index, char in enumerate(msg):
        rindex = index + starting_index
        final += colorize(
            char,
            fg=colors[rainbow[rindex % len(rainbow)]],
        )
    return final


def duration(seconds):
    d = datetime.datetime(1, 1, 1) + seconds
    fstr = ""
    if d.day - 1 > 0:
        if d.day - 1 == 1:
            fstr += "%d day " % (d.day - 1)
        else:
            fstr += "%d days " % (d.day - 1)
    if d.hour > 0:
        if d.hour == 1:
            fstr += "%d hour " % d.hour
        else:
            fstr += "%d hours " % d.hour
    if d.minute > 0:
        if d.minute == 1:
            fstr += "%d minute " % d.minute
        else:
            fstr += "%d minutes " % d.minute
    if d.second > 0:
        if d.second == 1:
            fstr += "%d second " % d.second
        else:
            fstr += "%d seconds " % d.second
    return fstr
