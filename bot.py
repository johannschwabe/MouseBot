import telegram
from requests import Response
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, Dispatcher, ContextTypes
import datetime
import requests
import json
import traceback
import sys

protocol = "http"
ip = "192.168.188.116"
port = "8000"
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


def status(update: telegram.Update, context: CallbackContext):
    res: "Response" = requests.get(f"{protocol}://{ip}:{port}/status")
    context.bot.send_message(chat_id=update.message.chat_id, text=res.json()["status"])


def remove(update: telegram.Update, context: CallbackContext):
    data = {"trap_name": context.args[0]}
    res = requests.post(f"{protocol}://{ip}:{port}/remove", data=json.dumps(data),
                        headers={"Content-Type": "application/json"})
    if res.status_code < 300:
        update.message.reply_text("👍")
    else:
        update.message.reply_text("👎")


def rename(update: telegram.Update, context: CallbackContext):
    if len(context.args) != 2:
        update.message.reply_text("👎")
    data = {"old": context.args[0], "new": context.args[1]}
    res = requests.post(f"{protocol}://{ip}:{port}/rename", data=json.dumps(data),
                        headers={"Content-Type": "application/json"})
    if res.status_code < 300:
        update.message.reply_text("👍")
    else:
        update.message.reply_text("👎")


def unknown(update: telegram.Update, context: CallbackContext):
    update.message.reply_text("🤯")


if __name__ == '__main__':
    # Read my personal bot token out of the token.txt file which is not uploaded to GitHub, and hand it to the updater.

    f = open(".secrets", "r")
    token = f.readlines()[0]
    updater = Updater(token)
    dispatcher: "Dispatcher" = updater.dispatcher

    # Tell dispatcher which functions are to execute according to which user commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("status", status))
    dispatcher.add_handler(CommandHandler("remove", remove, pass_args=True))
    dispatcher.add_handler(CommandHandler("rename", rename, pass_args=True))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    for chat_id in chat_ids:
        updater.bot.send_message(text="hi", chat_id=chat_id)

    # Start bot
    updater.start_polling()

    # Keep the bot alive even though nobody is requesting anything
    updater.idle()
