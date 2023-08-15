from telebot import *
from setup import *

bot = TeleBot(token)

def edit_message(message: types.Message, text: str, reply_markup=None):
  try:
    bot.edit_message_text(text, message.chat.id, message.id, reply_markup=reply_markup)
  except Exception as e:
    print(e)