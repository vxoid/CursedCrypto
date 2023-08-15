from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from telebot import types
from urllib import parse
from setup import *
from texts import *
import feedparser

password = parse.quote(password, safe="")

engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")
Base = declarative_base()

delete_feed_data = "delfeed"
feed_back_data = "feedback"

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
  
  def create_message(self) -> str:
    feed = feedparser.parse(self.url)

    entries = f" ({len(feed.entries)})" if len(feed.entries) > 0 else ""
    message = f"RSS Feed - {self.url}{entries}\n"
    try:
      message += f"Last post at {feed.entries[0].published}"
    except IndexError:
      pass

    return message
  
  def create_markup(self) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()

    delete_button = types.InlineKeyboardButton(delete_button_content, callback_data=f"{delete_feed_data}{self.id}")
    back_button = types.InlineKeyboardButton(back_button_content, callback_data=feed_back_data)

    return markup.add(delete_button, back_button)
  
  def __str__(self) -> str:
    return str(self.url)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)