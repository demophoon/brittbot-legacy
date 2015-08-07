#!/usr/bin/env python
# encoding: utf-8

import datetime

from textblob import TextBlob

from sqlalchemy import create_engine
from sqlalchemy import (
    Column,
    Integer,
    Text,
    Float,
    DateTime,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    nick = Column(Text)
    body = Column(Text)
    room = Column(Text)
    created_at = Column(DateTime)
    polarity = Column(Float)
    subjectivity = Column(Float)

    def __init__(self, nick, room, msg):
        try:
            tb = TextBlob(msg)
            self.polarity = tb.sentiment.polarity
            self.subjectivity = tb.sentiment.subjectivity
        except Exception:
            pass
        self.nick = nick
        self.room = room
        self.body = msg
        self.created_at = datetime.datetime.utcnow()


def db_logger(jenni, msg):
    message = Message(msg.nick, msg.sender, msg)
    jenni.db.add(message)
    jenni.db.commit()
db_logger.rule = r'.*'
db_logger.priority = 'high'


def create_session(db_conn):
    engine = create_engine(db_conn)
    Base.metadata.create_all(engine)
    Session = sessionmaker(autoflush=False)
    Session.configure(bind=engine)
    return Session()


def setup(jenni):
    if not hasattr(jenni.config, 'sqlalchemy_database_uri'):
        print("Please specify a 'sqlalchemy_database_uri' "
              "string in your configuration to use the database module")
        return
    jenni.db = create_session(jenni.config.sqlalchemy_database_uri)
