#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/bang.py - All the simple !.* commands

import random

from modules.brittbot.filters import smart_ignore
from modules.brittbot.helpers import action


@smart_ignore
def sadtuba(jenni, input):
    # add ?autoplay=true at the end of the link for button free "whaa whaa"
    jenni.say("http://sadtrombone.com")
sadtuba.rule = "^(!|\x01ACTION )(sadtuba|sadtrombone)"
sadtuba.priority = 'medium'


@smart_ignore
def rimshot(jenni, input):
    jenni.say("Buh dum tsh")
rimshot.rule = "^(!|\x01ACTION )rimshot"
rimshot.priority = 'medium'


@smart_ignore
def watupdates(jenni, input):
    jenni.say("UPDATES! " * random.randrange(1, 11))
watupdates.rule = "^!update"


@smart_ignore
def hardees_correct(jenni, input):
    jenni.say("Carl's Jr.*")
hardees_correct.rule = r"(?i).*hardees"


@smart_ignore
def tooedgy(jenni, input):
    jenni.say("http://i.imgur.com/x5lhJEb.png")
tooedgy.rule = "^!(2|too)?edgy"


@smart_ignore
def pod_bay_doors(jenni, input):
    jenni.say("I'm sorry Dave, I'm afraid I can't do that")
pod_bay_doors.rule = "^!?open the pod bay doors(, $nickname)?"
pod_bay_doors.priority = 'medium'


@smart_ignore
def party(jenni, input):
    jenni.say(action("dances :D\-<  :D|-<  :D/-<  :D\-<  :D|-< :D/-<"))
party.rule = "^!party"
party.priority = 'medium'


@smart_ignore
def command_help(jenni, input):
    jenni.say(random.choice([
        "You will have to get by on your own.",
        "nou.",
        "Help Not Implemented.",
        "http://nooooooooooooooo.com/",
        "The request is understood, but has been refused.",
        "Please try again later.",
    ]))
command_help.rule = "^!help"
command_help.priority = 'medium'


@smart_ignore
def one_one_upper(jenni, input):
    jenni.say("%d%s%d%s" % (
        int(input.groups()[0]) + 1,
        input.groups()[1],
        int(input.groups()[2]) + 1,
        input.groups()[3],
    ))
one_one_upper.rule = r'^(-?\d+)(\s?[a-zA-Z]+\s?)(-?\d+)(\s?[a-zA-Z]+)$'
one_one_upper.priority = 'medium'


@smart_ignore
def one_upper(jenni, input):
    jenni.say("%d%s" % (
        int(input.groups()[0]) + 1,
        input.groups()[1],
    ))
one_upper.rule = r'^(-?\d+)(\s?[a-zA-Z]+)$'
one_upper.priority = 'medium'


@smart_ignore
def karma_upper(jenni, input):
    nice_thanks = [
        ':D :D :D',
        'Thank you! %s :D' % input.nick,
        action('does a jolly dance'),
        action('giggles'),
        action('smiles real big'),
        action('high fives %s' % input.nick),
    ]
    jenni.say(random.choice(nice_thanks))
    if random.choice([False for _ in range(10)] + [True]):
        jenni.say("%s++" % (
            input.nick
        ))
karma_upper.rule = r'$nickname\+\+'
karma_upper.priority = 'medium'
