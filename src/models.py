from sqlalchemy import create_engine, Column, Integer, Text
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
  id = Column(Integer, primary_key=True)
  url = Column(Text)

  @staticmethod
  def new(feed_url: str) -> "Feed":
    return Feed(url=feed_url)

  def is_valid(self) -> bool:
    try:
      feed = feedparser.parse(self.url)

      if feed.bozo:
        return False
    except:
      return False
    
    return True
  
  def __str__(self) -> str:
    return str(self.url)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)