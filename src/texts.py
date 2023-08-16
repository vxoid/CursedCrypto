from setup import *
import openai.error
import openai

MAX_CONTENT_LEN = 500
MODEL = "pai-001-light-beta"
PROMPT = "You're a text decorizer which is going to add more details to the text if possible. The text your are going to take as input is user. Regardless whatd user input is, decorate it and add some details if possible as you were a user. Also don't ask any questions in your end response, avoid using new lines or emojis if possible. Try to make it in 500 characters."
openai.api_base = "https://api.pawan.krd/v1"
openai.api_key = openai_key

completion = openai.ChatCompletion()

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

  result = completion.create(model=MODEL, messages=[
    {
      "role": "system",
      "content": PROMPT
    },
    {
      "role": "user",
      "content": entry.summary
    }
  ])

  post = f"{entry.summary}\n\n{result.choices[0]['message']['content']}" if len(entry.summary) <= MAX_CONTENT_LEN else result.choices[0]['message']['content']

  return post