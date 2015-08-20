#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/approval.py - Sentiment analysis

from textblob import TextBlob


def approval_rating(jenni, msg):
    try:
        analysis = TextBlob(str(msg))
    except Exception:
        return
    if 'approval' not in jenni.brain:
        jenni.brain['approval'] = {}
    if msg.nick not in jenni.brain['approval']:
        jenni.brain['approval'][msg.nick] = 0
    jenni.brain['approval'][msg.nick] += analysis.sentiment.polarity
    jenni.brain.save()
    print "Approval rating from {}: {} ({})".format(
        msg.nick,
        jenni.brain['approval'][msg.nick],
        analysis.sentiment.polarity,
    )
approval_rating.rule = r".*$nickname.*"
approval_rating.wrapped = False


def room_rating(jenni, msg):
    try:
        analysis = TextBlob(str(msg))
    except Exception:
        return
    if 'approval_room' not in jenni.brain:
        jenni.brain['approval_room'] = {}
    if msg.sender not in jenni.brain['approval_room']:
        jenni.brain['approval_room'][msg.sender] = {}
    if msg.nick not in jenni.brain['approval_room'][msg.sender]:
        jenni.brain['approval_room'][msg.sender][msg.nick] = {'msgs': 0, 'score': 0}
    if analysis.sentiment.subjectivity < .5:
        return
    jenni.brain['approval_room'][msg.sender][msg.nick]['msgs'] += 1
    jenni.brain['approval_room'][msg.sender][msg.nick]['score'] += analysis.sentiment.polarity
room_rating.rule = r".*"
room_rating.wrapped = False


def how_happy_is_room(jenni, msg):
    if not msg.admin:
        return
    room = msg.groups()[0]
    final_score = 0
    highest_score = 0
    highest_user = None
    lowest_score = 0
    lowest_user = None
    if room in jenni.brain['approval_room']:
        for user in jenni.brain['approval_room'][room]:
            if jenni.brain['approval_room'][room][user]['msgs'] <= 25:
                continue
            score = jenni.brain['approval_room'][room][user]['score'] / jenni.brain['approval_room'][room][user]['msgs']
            score *= 100
            if not (highest_user and lowest_user):
                highest_user = user
                highest_score = score
                lowest_user = user
                lowest_score = score
            if score > highest_score:
                highest_score = score
                highest_user = user
            if score < lowest_score:
                lowest_score = score
                lowest_user = user
            final_score += score
        reply = room
        if final_score > 0:
            reply += " is generally a positive room"
        else:
            reply += " is generally a negative room"
        reply += " (%0.2f)." % (final_score, )
        reply += " The most positive person in the room is %s (%0.2f) and " % (
            highest_user,
            highest_score,
        )
        reply += "it seems the most negative person in the room is %s (%0.2f)." % (
            lowest_user,
            lowest_score,
        )
    elif room in jenni.brain['approval_room'][msg.sender]:
        score = jenni.brain['approval_room'][msg.sender][room]['score'] / jenni.brain['approval_room'][msg.sender][room]['msgs']
        score *= 100
        reply = "{} approval score is {}.".format(
            room,
            '%0.2f' % (score),
        )
    jenni.reply(reply)
how_happy_is_room.rule = r"!approval (\S+)"


def how_happy_am_i(jenni, msg):
    room = msg.sender
    nick = msg.nick
    approvals = jenni.brain['approval_room'][room]
    approvals[msg.nick],
    if nick not in approvals:
        return
    if approvals[nick]['msgs'] <= 0:
        return
    samples = approvals[nick]['msgs']
    score = approvals[nick]['score'] / samples
    score *= 100
    jenni.reply("Your approval score is: %0.2f with %s samples" % (score, samples))
how_happy_am_i.rule = r"!approval$"


def arewefriends(jenni, msg):
    if msg.friend:
        reply = "Yes"
    else:
        reply = "No"
    jenni.reply(reply)
arewefriends.rule = r"(?i)^$nickname\W? (?:are you my|am i your|are we) friends?\??"
