#!/usr/bin/env python
# encoding: utf-8
# jenni db.py - Database layer for brittbot

return

import datetime
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()


def get_current_time():
    return datetime.datetime.now()


class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    room_id = Column(Integer, ForeignKey("room.id"))
    body = Column(String(convert_unicode=True))
    created_at = Column(DateTime)

    def __init__(self):
        self.created_at = get_current_time()


class Room(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    messages = relationship("Message", backref="room")


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    nick = Column(String)
    access = Column(String)
    messages = relationship("Message", backref="user")


class Quote(Base):
    __tablename__ = 'quote'
    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, ForeignKey("message.id"))
    grabbed_by = Column(Integer, ForeignKey("user.id"))
    message = relationship("Message")
    who_grabbed = relationship("User", backref="quotes")
    created_at = Column(DateTime)

    def __init__(self):
        self.created_at = get_current_time()


class Point(Base):
    __tablename__ = 'point'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    awarded_by_id = Column(Integer, ForeignKey(User.id))
    type = Column(String)
    created_at = Column(DateTime)
    value = Column(Integer)

    user = relationship("User", backref="points", foreign_keys=user_id)
    awarded_by = relationship(
        "User", backref="awarded_points", foreign_keys=awarded_by_id)

    def __init__(self, type, user_id, awarded_by_id, value=1):
        start_time = get_current_time() - datetime.timedelta(minutes=10)
        user = DBSession.query(User).filter(
            User.id == user_id
        ).first()
        if sum(
            [x.value for x in user.points if x.created_at > start_time]
        ) > 20:
            value = 0
        if sum(
            [x.value for x in user.awarded_points if x.created_at > start_time]
        ) > 20:
            value = 0
        self.created_at = get_current_time()
        self.type = type
        self.user_id = user_id
        self.awarded_by_id = awarded_by_id
        self.value = value


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    tagged_by_id = Column(Integer, ForeignKey(User.id))
    created_at = Column(DateTime)
    tagged = Column(Integer)

    user = relationship("User", backref="tags", foreign_keys=user_id)
    awarded_by = relationship(
        "User", backref="tagged", foreign_keys=tagged_by_id)

    def __init__(self):
        self.created_at = get_current_time()


class Audit(Base):
    __tablename__ = 'audit'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    message_id = Column(Integer, ForeignKey("message.id"))

    user = relationship("User", backref="audits")
    message = relationship("Message", backref="audit")


# ----- end models -

DBSession = None

engine = create_engine("sqlite:///irclog.db")
DBSession = scoped_session(sessionmaker(bind=engine))
Base.metadata.create_all(engine)
