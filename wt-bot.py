from telegram.ext import Updater, CommandHandler
import requests
import re

from tk import get_token

def main():
    token = get_token()
    updater = Update(token)

def command1():
    data = get_data()
    chat_id = update.message.chat_id
    bot.send(chat_id=chat_id)

def get_data():
    data = {"text1":"Hello World"}
    return data

