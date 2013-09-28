#!/usr/bin/env python
#-*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String
from database import Base

class Entries(Base):
   __tablename__ = 'entries'
   twitter_id = Column('twitter_id', Integer, primary_key=True)
   oauth_token = Column('oauth_token', String(200))
    
   def __init__(self, twitter_id=None, oauth_token=None):
        self.twitter_id = twitter_id
        self.oauth_token = oauth_token

   def __repr__(self):
        return '<Entries>'

   
class Stack(Base):
   __tablename__ = 'stack'
   stack_id = Column('stackid', Integer, primary_key=True)
   twitter_id = Column('twitter_id', Integer)
   text = Column('text', String(450))
   datetime = Column('datetime', String(30))
   
   def __init__(self, twitter_id=None, text=None, datetime=None):
      self.twitter_id = twitter_id
      self.text = text
      self.datetime = datetime

   def __repr__(self):
      return '<Stack>'
