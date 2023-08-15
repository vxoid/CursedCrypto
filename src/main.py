from multiprocessing import Process
from notifier import *

if __name__ == "__main__":
  process = Process(target=notify)
  process.start()

  bot.polling()