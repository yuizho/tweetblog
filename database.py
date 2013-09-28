#!/usr/bin/env python
#-*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE   = 'sqlite:////tmp/tweet_stacker.db'

#setup sqlalchemy
engine = create_engine(DATABASE)
#metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
   Base.metadata.create_all(bind=engine)
