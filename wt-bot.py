import logging
import textwrap

from telegram.ext import Updater, CommandHandler
from telegram.error import TelegramError
import requests

from tk import get_token
from api_key import get_api_key

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)

def main():
    access_token = get_token()
    updater = Updater(token=access_token, use_context=True)
    dispatcher = updater.dispatcher
    
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    track_handler = CommandHandler('track', track)
    dispatcher.add_handler(track_handler)

    dispatcher.add_error_handler(error_callback)

    updater.start_polling()

def start(update, context):
    output = '''
                Hi! I'm WeatherTrack bot!
                Use _/track <city name>, <country code (optional)>_
                to obtain a city's latest weather report.
             '''

    output = textwrap.dedent(output)

    context.bot.send_message(chat_id=update.effective_chat.id, parse_mode='Markdown', text=output)

def track(update, context):
    api_key = get_api_key()

    query = {'q': ' '.join(context.args), 'appid': api_key, 'units':'metric'}
    response = requests.get('https://api.openweathermap.org/data/2.5/weather', params=query)
    
    if response.status_code == 200:
        data = response.json()
    
        output = f'''
                    *Weather Report of {data['name']}, {data['sys']['country']}*
                    - - - - -
                    *Weather group:* {data['weather'][0]['main']}
                    *Weather condition:* {data['weather'][0]['description'].capitalize()}
                    *Current temperature:* {data['main']['temp']} \N{DEGREE SIGN}C
                    *Feels like:* {data['main']['feels_like']} \N{DEGREE SIGN}C
                    *Atmospheric pressure:* {data['main']['pressure']} hPa
                    *Humidity:* {data['main']['humidity']}%
                 '''

        output = textwrap.dedent(output)

        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode='Markdown', text=output)
    else:
        output = '''
                    No data found.
                    Please enter the command in the following format:
                    _/track <city name>, <country code (optional)>_
                    *Example:* _/track Paris_ or _/track Paris, FR_
                 '''
        
        output = textwrap.dedent(output)

        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode='Markdown', text=output)

def error_callback(update, context):
    try:
        raise context.error
    except TelegramError as error:
        output = f'''
                    Error: {error}.
                    Please try again.
                 '''
        
        output = textwrap.dedent(output)

        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode='Markdown', text=output)

if __name__ == '__main__':
    main()