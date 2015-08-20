#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/howmany.py - So many.

import random
from textblob import TextBlob


def how_many_x(jenni, msg):
    many = msg.groups()[0]
    subjects = TextBlob(str(msg.groups()[1])).noun_phrases.pluralize()
    if subjects:
        subject = random.choice(subjects)
        many = "many"
    else:
        subject = msg.groups()[1]
    if subject and len(subject.split(" ")) > 3:
        return
    if not subject:
        subject = ""
    so = "so"
    if subject == "cooks":
        so = "too"
        many = "many"
    if "second" in subject:
        so = "just"
        many = "one"
        subject = "second"
    if "fuck" in subject:
        so = "no"
        many = "fucks"
        subject = "given"
    if "brittbot" in subject.lower().split(" "):
        subject = subject.lower().replace("brittbot", msg.nick.lower())
    elif "i" in subject.lower().split(" "):
        subject = subject.lower().replace("i", "you")
    jenni.say("{} {} {}".format(so, many, subject))
how_many_x.rule = r"(?i)how (few|many|much) ?([a-zA-Z\s]+)?\??$"
