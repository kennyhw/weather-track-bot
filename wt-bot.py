import re

from telegram.ext import Updater, CommandHandler
import requests

from tk import get_token
from api_key import get_api_key

def main():
    access_token = get_token()
    updater = Updater(token=access_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    track_handler = CommandHandler('track', track)
    dispatcher.add_handler(track_handler)

    updater.start_polling()

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot. Beep boop.")

def track(update, context):
    output = ''
    api_key = get_api_key()

    query = {'q': 'Singapore', 'appid': api_key}
    data = requests.get('https://api.openweathermap.org/data/2.5/weather', params=query)
    
if __name__ == '__main__':
    main()