#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import create_engine
from sqlalchemy import (
    Column,
    Integer,
    Text,
    Float,
    DateTime,
)
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declaritive import declarative_base

engine = None
DBSession = None


class Message:
    pass


def setup_test(jenni):
    global engine
    global DBSession
    global Message

    engine = create_engine(
        jenni.config['sqlalcmemy_database_uri'],
        convert_unicode=True,
    )
    DBSession = scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
        )
    )

    Base = declarative_base()
    Base.query = DBSession.query_property()

    class Message(Base):
        __tablename__ = "messages"
        id = Column(Integer, primary_key=True)
