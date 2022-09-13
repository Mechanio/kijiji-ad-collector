from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from config import Config

db_string = Config.SQLALCHEMY_DATABASE_URI

db = create_engine(db_string)
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=db))

base = declarative_base()

# Session = sessionmaker(db)
base.query = Session.query_property()
session = Session()
