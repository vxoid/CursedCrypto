from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from telebot import types
from urllib import parse
from setup import *
from texts import *
import feedparser
import time

password = parse.quote(password, safe="")

engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")
Base = declarative_base()

delete_feed_data = "delfeed"
feed_back_data = "feedback"

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_STR = ""

class Feed(Base):
  __tablename__ = "feeds"
  id = Column(Integer, primary_key=True)
  url = Column(Text)
  latest_published = Column(Text)

  @staticmethod
  def new(feed_url: str) -> "Feed | None":
    feed = Feed(url=feed_url)
    try:
      parsed_feed = feedparser.parse(feed_url)
    except:
      return None
    
    if parsed_feed.bozo:
      return None
    
    feed.latest_published = DEFAULT_STR
    for entry in parsed_feed.entries[1:]:
      try:
        published = entry.published_parsed
      except AttributeError:
        continue

      if feed.latest_published == DEFAULT_STR:
        feed.latest_published = time.strftime(TIME_FORMAT, published)
        continue
      
      if published > time.strptime(feed.latest_published, TIME_FORMAT):
        feed.latest_published = time.strftime(TIME_FORMAT, published)

    return feed

  def is_valid(self) -> bool:
    try:
      feed = feedparser.parse(self.url)
    except:
      return False
    
    if feed.bozo:
      return False
    
    return True
  
  def create_message(self) -> str:
    feed = feedparser.parse(self.url)

    entries = f" ({len(feed.entries)})" if len(feed.entries) > 0 else ""
    message = f"RSS Feed - {self.url}{entries}\n"
    if str(self.latest_published) != DEFAULT_STR:
      message += f"Last post at {self.latest_published}"

    return message
  
  def create_markup(self) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()

    delete_button = types.InlineKeyboardButton(delete_button_content, callback_data=f"{delete_feed_data}{self.id}")
    back_button = types.InlineKeyboardButton(back_button_content, callback_data=feed_back_data)

    return markup.add(delete_button, back_button)
  
  def __str__(self) -> str:
    return str(self.url)
  
class Post(Base):
  __tablename__ = "posts"
  id = Column(Integer, primary_key=True)
  content = Column(Text)
  title = Column(Text)
  link = Column(Text)

  def create_message(self) -> str:
    message = f"{self.title}\n\n"
    if str(self.content):
      message += f"{self.content}\n"
    message += f"P.S. [Original post]({self.link})"

    return message

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)