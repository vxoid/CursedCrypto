from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib import parse
from youtube import *
from telebot import *
from loadenv import *

password = parse.quote(password, safe="")

engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")
Base = declarative_base()
video_url_pattern = r"(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))([^&?\/\s]{11})"

class Url(Base):
  __tablename__ = "urls"
  id = Column(Integer, primary_key=True)

  owner_telegram_id = Column(Text)
  comments = Column(Integer)
  video_url = Column(Text)

  def is_commented_by(self, channel_id: str, from_time: datetime):
    comments = Comment.get_video_comments(self.get_video_id())

    for comment in comments:
      if comment.author.channel_id == channel_id and comment.published_at > from_time:
        return True
      
    return False

  @staticmethod
  def is_valid_video_link(link: str):
    match = re.search(video_url_pattern, link)

    return match

  def get_video_id(self) -> str:
    match = re.search(video_url_pattern, self.video_url)
    
    video_id = match.group(1)
    return video_id

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()