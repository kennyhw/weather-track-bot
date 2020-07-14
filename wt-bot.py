import re
import textwrap

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
    api_key = get_api_key()

    query = {'q': 'Singapore', 'appid': api_key, 'units':'metric'}
    response = requests.get('https://api.openweathermap.org/data/2.5/weather', params=query)

    data = response.json()
    
    output = f'''\
                *{data['name']} Weather Report*
                --------------------
                *Weather group:* {data['weather'][0]['main']}
                *Weather condition:* {data['weather'][0]['description'].capitalize()}
                *Current temperature:* {data['main']['temp']} \N{DEGREE SIGN}C
                *Feels like:* {data['main']['feels_like']} \N{DEGREE SIGN}C
                *Atmospheric pressure:* {data['main']['pressure']} hPa
                *Humidity:* {data['main']['humidity']}%
             '''

    output = textwrap.dedent(output)

    context.bot.send_message(chat_id=update.effective_chat.id, parse_mode='Markdown', text=output)

    
if __name__ == '__main__':
    main()