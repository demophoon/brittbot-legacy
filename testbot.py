#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import signal

import configs
import bot
import irc


class Watcher(object):
    def __init__(self):
        self.child = os.fork()
        if self.child != 0:
            self.watch()

    def watch(self):
        try:
            os.wait()
        except KeyboardInterrupt:
            self.kill()
        sys.exit()

    def kill(self):
        try:
            os.kill(self.child, signal.SIGKILL)
        except OSError:
            pass


class MockBot(bot.Jenni):

    def write(self, args, text=None, raw=False):
        print text

    def msg(self, recipient, text, log=False, x=False, wait_time=3):
        print u"{}: {}".format(recipient, text)


def get_jenni(config_path):
    config_files = []

    config = configs.Configs([config_path])
    config.load_modules(config_files)

    try:
        Watcher()
    except Exception, e:
        print >> sys.stderr, 'Warning:', e, '(in __init__.py)'

    jenni = MockBot(config_files[0])
    return jenni


def message(jenni, hostmask, room, msg):
    origin = irc.Origin(
        jenni,
        hostmask,
        [
            "PRIVMSG",
            room,
            msg,
        ]
    )
    jenni.dispatch(origin, [
        msg,
        'PRIVMSG',
    ])
