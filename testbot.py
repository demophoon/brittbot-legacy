#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import signal
import time

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

    recieved_messages = {}

    def write(self, args, text=None, raw=False):
        print u"{}: {}".format(self.uuid, text)

    def msg(self, recipient, text, log=False, x=False, wait_time=3):
        if self.uuid not in self.recieved_messages:
            self.recieved_messages[self.uuid] = []
        self.recieved_messages[self.uuid].append({
            'room': recipient,
            'message': text,
        })
        print u"{}: {}".format(recipient, text)

    def send(self, msg, room="##test", hostmask="example!test@localhost"):
        origin = irc.Origin(
            self,
            hostmask,
            [
                "PRIVMSG",
                room,
                msg,
            ]
        )
        task_ids = self.dispatch(origin, [
            msg,
            'PRIVMSG',
        ])
        responses = []
        for _ in range(10):
            for task_id in task_ids:
                response = self.recieved_messages.get(task_id)
                if not response:
                    continue
                responses += response
            if responses:
                break
            time.sleep(0.1)
        responses = [x.get('message', "") for x in responses]
        return '\n'.join(responses)


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

if __name__ == '__main__':
    jenni = get_jenni("/home/britt/.jenni/default.py")
