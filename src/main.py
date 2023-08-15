from multiprocessing import Process
from main_menu import *
from notifier import *

@bot.message_handler(commands=["start"], func=lambda message: message.from_user.id == owner)
def start(message: types.Message):
  bot.send_message(message.chat.id, start_message, reply_markup=main_markup)

if __name__ == "__main__":
  process = Process(target=notify)
  process.start()

  bot.polling()