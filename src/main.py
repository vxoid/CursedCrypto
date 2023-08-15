from multiprocessing import Process
from notifier import *

add_feed_data = "addfeed"
feeds_data = "feeds"

main_markup = types.InlineKeyboardMarkup()

add_feed_button = types.InlineKeyboardButton(text=add_feed_button_content, callback_data=add_feed_data)
feeds_button = types.InlineKeyboardButton(text=feeds_button_content, callback_data=feeds_data)

main_markup.add(add_feed_button)

@bot.message_handler(commands=["start"], func=lambda message: message.from_user.id == owner)
def start(message: types.Message):
  bot.send_message(message.chat.id, start_message)

if __name__ == "__main__":
  process = Process(target=notify)
  process.start()

  bot.polling()