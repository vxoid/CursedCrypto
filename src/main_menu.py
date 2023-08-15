from cancel import *
from models import *

add_feed_data = "addfeed"
feeds_data = "feeds"
view_feed_data = "viewfeed"
set_feed_page_data = "setfeedpage"

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


@bot.callback_query_handler(func=lambda call: call.data == feeds_data and call.from_user.id == owner)
def view_feeds(call: types.CallbackQuery):
  bot.send_message(call.message.chat.id, feeds_message, reply_markup=create_paged_markup(get_feeds_as_buttons(), 1, set_feed_page_data))
  bot.answer_callback_query(call.id, feeds_message)

def get_feeds_as_buttons() -> List[types.InlineKeyboardButton]:
  session = Session()

  feeds = session.query(Feed).all()
  buttons = [types.InlineKeyboardButton(str(feed), callback_data=f"{view_feed_data}{feed.id}") for feed in feeds]

  return buttons

@bot.callback_query_handler(func=lambda call: call.data.startswith(view_feed_data) and call.from_user.id == owner)
def view_feed(call: types.CallbackQuery):
  id = int(call.data.removeprefix(view_feed_data))

  session = Session()

  feed = session.query(Feed).filter(Feed.id == id).first()
  if feed is None:
    bot.answer_callback_query(call.id, invalid_feed_message)
    return
  
  edit_message(call.message, feed.create_message(), feed.create_markup())

@bot.callback_query_handler(func=lambda call: call.data.startswith(set_feed_page_data) and call.from_user.id == owner)
def set_page(call: types.CallbackQuery):
  page = int(call.data.removeprefix(set_feed_page_data))

  edit_message(call.message, feeds_message, create_paged_markup(get_feeds_as_buttons(), page, set_feed_page_data))

@bot.callback_query_handler(func=lambda call: call.data.startswith(delete_feed_data) and call.from_user.id == owner)
def delete(call: types.CallbackQuery):
  id = int(call.data.removeprefix(delete_feed_data))

  session = Session()

  feed = session.query(Feed).filter(Feed.id == id).first()
  if feed is None:
    bot.answer_callback_query(call.id, invalid_feed_message)
    return
  
  session.delete(feed)
  session.commit()
   
  bot.delete_message(call.message.chat.id, call.message.id)

@bot.callback_query_handler(func=lambda call: call.data == feed_back_data and call.from_user.id == owner)
def back(call: types.CallbackQuery):
  edit_message(call.message, feeds_message, reply_markup=create_paged_markup(get_feeds_as_buttons(), 1, set_feed_page_data))