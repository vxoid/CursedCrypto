from import_bot import *
from texts import *

cancel_markup = types.InlineKeyboardMarkup()

cancel_data = "cancel"
cancel_button = types.InlineKeyboardButton(cancel_button_content, callback_data=cancel_data)

cancel_markup.add(cancel_button)

ITEMS_PER_PAGE = 5

@bot.callback_query_handler(func=lambda call: call.data == cancel_data)
def cancel_sc(call: types.CallbackQuery):
  bot.clear_step_handler_by_chat_id(call.message.chat.id)
  bot.delete_message(call.message.chat.id, call.message.id)

def create_paged_markup(button_list: List[types.InlineKeyboardButton], current_page: int, prefix: str) -> types.InlineKeyboardMarkup:
  start_idx = (current_page - 1) * ITEMS_PER_PAGE
  end_idx = start_idx + ITEMS_PER_PAGE
  markup = types.InlineKeyboardMarkup()
  
  for button in button_list[start_idx:end_idx]:
    markup.add(button)
  
  if current_page > 1:
    markup.add(types.InlineKeyboardButton(previous_button_content, callback_data=f"{prefix}{current_page - 1}"))
  
  if end_idx < len(button_list):
    markup.add(types.InlineKeyboardButton(next_button_content, callback_data=f"{prefix}{current_page + 1}"))
  
  markup.add(cancel_button)
  return markup