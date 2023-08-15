from cancel import *
from models import *

add_feed_data = "addfeed"
feeds_data = "feeds"
view_feed_data = "viewfeed"

main_markup = types.InlineKeyboardMarkup()

add_feed_button = types.InlineKeyboardButton(text=add_feed_button_content, callback_data=add_feed_data)
feeds_button = types.InlineKeyboardButton(text=feeds_button_content, callback_data=feeds_data)

main_markup.add(add_feed_button, feeds_button)

@bot.callback_query_handler(func=lambda call: call.data == add_feed_data and call.from_user.id == owner)
def add_feed(call: types.CallbackQuery):
  session = Session()

  msg = bot.send_message(call.message.chat.id, add_feed_message, reply_markup=cancel_markup)
  bot.answer_callback_query(call.id, add_feed_message)

  def callback(message: types.Message):
    bot.delete_message(message.chat.id, message.id)

    feed_url = message.text or message.caption or ""

    feed = Feed.new(feed_url)
    
    if not feed.is_valid():
      edit_message(msg, invalid_add_feed_message.format(feed_url), reply_markup=cancel_markup)
      bot.register_next_step_handler(msg, callback=callback)
      return
    
    session.add(feed)
    session.commit()
    
    bot.delete_message(msg.chat.id, msg.id)

  bot.register_next_step_handler(msg, callback=callback)

def get_feeds_as_buttons() -> List[types.InlineKeyboardButton]:
  session = Session()

  feeds = session.query(Feed).all()
  buttons = [types.InlineKeyboardButton(str(feed), callback_data=f"{view_feed_data}{feed.id}") for feed in feeds]

  return buttons