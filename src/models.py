from sqlalchemy import create_engine, Column, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib import parse
from setup import *
import feedparser

password = parse.quote(password, safe="")

engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")
Base = declarative_base()

class Feed(Base):
  __tablename__ = "feeds"
  url = Column(Text)

  def is_valid(self) -> bool:
    try:
      feed = feedparser.parse(self.url)
      if not "entries" in feed:
        return False
    except:
      return False
    
    return True

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()