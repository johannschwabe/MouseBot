import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import datetime
import requests
import json
import traceback
import sys

protocol = "http"
ip = "localhost"
port = "8182"
chat_ids = []

# Define the funciton that shall be executed on Start command /start, which is automatically send when starting the bot
def start(update: telegram.Update, context: CallbackContext):
    # Sending some welcome messages and instructions about the bot usage
    context.bot.send_message(chat_id=update.message.chat_id,
                     text='Action Stations!',
                     parse_mode=telegram.ParseMode.MARKDOWN)
    if update.message.chat_id not in chat_ids:
        chat_ids.append(update.message.chat_id)
        t = open("chat_ids.txt", "a")
        t.write(f"{str(update.message.chat_id)}\n")


if __name__ == '__main__':
    # Read my personal bot token out of the token.txt file which is not uploaded to github, and hand it to the updater.
    t = open("chat_ids.txt","r")
    chat_ids = [int(_id) for _id in t.readlines()]
    f = open(".secrets", "r")
    token = f.readlines()[0]
    updater = Updater(token)
    dispatcher = updater.dispatcher

    # Tell dispatcher which functions are to execute according to which user commands
    dispatcher.add_handler(CommandHandler("start", start))

    # Start bot
    updater.start_polling()

    # Keep the bot alive even though nobody is requesting anything
    updater.idle()