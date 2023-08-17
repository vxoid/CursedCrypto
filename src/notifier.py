from import_bot import *
from models import *

INTERVAL = 10

def notify():
  session = Session()
  
  while True:
    feeds = session.query(Feed).all()

    for unparsed_feed in feeds:
      feed = feedparser.parse(unparsed_feed.url)

      for entry in feed.entries:
        try:
          try:
            published = entry.published_parsed
          except AttributeError:
            continue

          is_latest = published >= time.strptime(str(unparsed_feed.latest_published), TIME_FORMAT) if str(unparsed_feed.latest_published) != DEFAULT_STR else True

          if is_latest:
            unparsed_feed.latest_published = time.strftime(TIME_FORMAT, published)
            session.commit()

            if session.query(Post).filter(Post.link == entry.link).first() is not None:
              continue
            
            title = create_entry_title(entry)
            try:
              content = create_entry_content(entry, title)
            except openai.error.RateLimitError:
              continue

            post = Post(link = entry.link, title = title, content = content)

            session.add(post)
            session.commit()

            photo_url = None

            try:
              for attachment in entry.media_content:
                try:
                  if attachment["medium"] == "image":
                    photo_url = attachment["url"]
                    break
                except KeyError:
                  pass
            except AttributeError:
              pass

            message = post.create_message()
            
            try:
              if photo_url is not None:
                bot.send_photo(channel, photo_url, message, parse_mode="Markdown")
              else:
                bot.send_message(channel, message, parse_mode="Markdown")
            except Exception as e:
              print(f"Can't send message due to: {e}")
        except Exception as e:
          bot.send_message(owner, f"Got error: {e}.\nCannot process [the entry]({entry.link}).", parse_mode="Markdown")
          
    time.sleep(INTERVAL)

