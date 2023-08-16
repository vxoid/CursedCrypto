from setup import *

start_message = "Hi there!"
add_feed_message = "Please enter rss feed url to add."
feeds_message = "Here is all feeds!"
invalid_add_feed_message = "'{}' is not a valid rss feed, try again using a valid rss feed."
invalid_feed_message = "Invalid feed"

add_feed_button_content = "Add feed! ➕"
feeds_button_content = "View feeds! 📄"
delete_button_content = "Delete 🗑️"
cancel_button_content = "Cancel ✖️"
back_button_content = "Back 🔙"
previous_button_content = "Previous ⏮️"
next_button_content = "Next ⏭️"

def create_entry_content(entry) -> str:
  if "summary" not in entry:
    return ""

  return entry.summary