#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/weissme.py - Weiss Me Nao

from modules.brittbot.filters import smart_ignore

weiss_img = "https://secure.gravatar.com/avatar/fd1e65538fa0a8d7e9b26274f9cab7ca?s=420#.png"


@smart_ignore
def weiss_me(phenny, msg):
    phenny.say(weiss_img)
weiss_me.rule = r"^!?weiss ?me$"
weiss_me.priority = 'medium'
