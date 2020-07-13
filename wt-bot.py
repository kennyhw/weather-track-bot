import re

from telegram.ext import Updater, CommandHandler
import requests

from tk import get_token

def main():
    access_token = get_token()
    updater = Updater(token=access_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    updater.start_polling()

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot. Beep boop.")

if __name__ == '__main__':
    main()