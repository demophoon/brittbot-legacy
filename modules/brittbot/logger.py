#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/logger.py - Logs messages for all rooms

import collections
import random

from modules.brittbot.db import (
    DBSession,
    Room,
    Message,
    User,
)


def logger(jenni, input):
    if not DBSession.query(User).filter(User.nick == input.nick).first():
        new_user = User()
        new_user.nick = input.nick
        DBSession.add(new_user)
    if not DBSession.query(Room).filter(Room.name == input.sender).first():
        new_room = Room()
        new_room.name = input.sender
        DBSession.add(new_room)
    user_id = DBSession.query(User).filter(User.nick == input.nick).first()
    room_id = DBSession.query(Room).filter(
        Room.name == input.sender).first()
    msg = Message()
    msg.body = input
    msg.user_id = user_id.id
    msg.room_id = room_id.id
    DBSession.add(msg)
    DBSession.flush()
    DBSession.commit()

    last_messages = DBSession.query(Message).join(Room).filter(
        Room.name == input.sender
    ).order_by(
        Message.created_at.desc()
    ).limit(10).all()

    common = collections.Counter(
        [x.body.strip() for x in last_messages]
    ).most_common(1)
    if common[0][0] == input.strip() and\
            common[0][1] >= 2 + random.choice(range(3)):
        if random.choice(range(10)) == 0:
            jenni.say(common[0][0])

logger.rule = r'(.*)'
logger.priority = 'low'
logger.thread = False
