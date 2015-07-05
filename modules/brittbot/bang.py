#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/bang.py - All the simple !.* commands

import random

from modules.brittbot.filters import smart_ignore
from modules.brittbot.helpers import action


@smart_ignore
def mgs_alert(jenni, input):
    jenni.say("http://brittg.com/zMJpt")
mgs_alert.rule = r'^!+$'
mgs_alert.priority = 'high'


@smart_ignore
def sadtuba(jenni, input):
    # add ?autoplay=true at the end of the link for button free "whaa whaa"
    jenni.say("http://sadtrombone.com")
sadtuba.rule = "^(!|\x01ACTION )sad(tuba|trombone|\w+)"
sadtuba.priority = 'medium'


@smart_ignore
def rimshot(jenni, input):
    jenni.say("Buh dum tsh")
rimshot.rule = "^(!|\x01ACTION )rimshot"
rimshot.priority = 'medium'


@smart_ignore
def fourofourd(jenni, input):
    jenni.say("http://www.homestarrunner.com/404error.html")
fourofourd.rule = "^(!|\x01ACTION )404'd"
fourofourd.priority = 'medium'


@smart_ignore
def contributing(jenni, input):
    jenni.say("https://github.com/demophoon/brittbot")
contributing.rule = "^!contributing"


@smart_ignore
def watupdates(jenni, input):
    jenni.say("UPDATES! " * random.randrange(1, 11))
watupdates.rule = "^!update"


@smart_ignore
def hardees_correct(jenni, input):
    jenni.say("Carl's Jr.*")
hardees_correct.rule = r"(?i).*hardees"


@smart_ignore
def do_it_live(jenni, input):
    jenni.say("http://rationalmale.files.wordpress.com/2011/09/doitlive.jpeg")
do_it_live.rule = r"(?i).*fuck it!"


@smart_ignore
def tooedgy(jenni, input):
    jenni.say("http://i.imgur.com/x5lhJEb.png")
tooedgy.rule = "^!(2|too)?edgy"


@smart_ignore
def pod_bay_doors(jenni, msg):
    jenni.say("I'm sorry {}, I'm afraid I can't do that".format(msg.nick))
pod_bay_doors.rule = "^open the pod bay doors(, $nickname)?"
pod_bay_doors.priority = 'medium'


@smart_ignore
def therethere(jenni, input):
    msg = u"(￣▽￣)ノ(╥﹏╥) there, there"
    if input.groups()[0]:
        msg += input.groups()[0]
    jenni.say(msg)
therethere.rule = "^!therethere(.*)"


@smart_ignore
def horse_to_duck(jenni, msg):
    htd = 0.00035092493
    horses = float(msg.groups()[0])
    ducks = horses / htd
    if ducks != 1:
        ducks = "{} ducks".format(ducks)
    else:
        ducks = "1 duck"
    jenni.reply("It takes {} to produce {} horsepower".format(ducks, horses))
horse_to_duck.rule = r'^!horsetoduck ([0-9\.]+)'


@smart_ignore
def duck_to_horse(jenni, msg):
    htd = 2849.61230882
    ducks = float(msg.groups()[0])
    horses = ducks / htd
    if horses != 1:
        horses = "{} horses".format(horses)
    else:
        horses = "1 horse"
    jenni.reply("It takes {} to produce {} duckpower".format(horses, ducks))
duck_to_horse.rule = r'^!ducktohorse ([0-9\.]+)'


@smart_ignore
def themoreyouknow(jenni, input):
    from modules.brittbot.helpers import (colors, colorize, colorize_msg)
    themoreyouknow1 = u"The More You Know"
    themoreyouknow2 = u"≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈"
    star = u"★"
    jenni.say(colorize(themoreyouknow1, fg=colors['blue']))
    jenni.say(colorize_msg(themoreyouknow2) + colorize(star, fg=colors['yellow']) )
themoreyouknow.rule = "^!themoreyouknow"


@smart_ignore
def party(jenni, input):
    jenni.say(action("dances :D\-<  :D|-<  :D/-<  :D\-<  :D|-< :D/-<"))
party.rule = "^!party"
party.priority = 'medium'


@smart_ignore
def define_Word(jenni, msg):
    from textblob import TextBlob
    words = msg.groups()[0]
    words = TextBlob(words).words
    jenni.reply(words[0].define()[0])
define_Word.rule = "^!define (.*)"


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
    a, b = (int(input.groups()[0]) + 1, int(input.groups()[2]) + 1)
    if a == 2 and b == 4:
        a = 3
        b = 5
    jenni.say("%d%s%d%s" % (
        a,
        input.groups()[1],
        b,
        input.groups()[3],
    ))
one_one_upper.rule = r'^(-?\d+)(\s?[a-zA-Z]+\s?)(-?\d+)(\s?[a-zA-Z]+)$'
one_one_upper.priority = 'medium'


@smart_ignore
def one_upper(jenni, input):
    a = int(input.groups()[0]) + 1
    if a == 2:
        a = 3
    jenni.say("%d%s" % (
        a,
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
