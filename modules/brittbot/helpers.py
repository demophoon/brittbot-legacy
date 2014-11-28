#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/helpers.py - Various methods for formatting messages

colors = {
    'white': '0',
    'black': '1',
    'blue': '2',
    'navy': '2',
    'green': '3',
    'red': '4',
    'brown': '5',
    'maroon': '5',
    'purple': '6',
    'orange': '7',
    'olive': '7',
    'yellow': '8',
    'light green': '9',
    'lime': '9',
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


def action(msg):
    msg = '\x01ACTION %s\x01' % msg
    return msg


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
    for index, char in enumerate(msg):
        color_tag = unicode("\x03")
        final += color_tag
        final += "%s%s" % (
            colors[rainbow[index % len(rainbow)]],
            char,
        )
        final += color_tag
    return action(final)


def duration(seconds):
    d = datetime.datetime(1,1,1) + seconds
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
