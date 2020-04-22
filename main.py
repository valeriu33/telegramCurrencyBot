import threading  # run multiple schedules at once
import schedule  # update the currency data without command
import time  # sleep() after running schedule in while True
from datetime import datetime, timedelta

import telegram  # send messages
from telegram.ext import Updater, CommandHandler  # handle commands

import string

from secrets import BOT_TOKEN, CHAT_ID, API_KEY  # a class where I keep my secrets ;)
from currency import Currency
from api_access import get_all_prices_from_API, get_price_from_API_for, get_all_prices_from_API_for_date


def run_schedules_on_bg_thread(interval=1):  # copied from here https://github.com/mrhwick/schedule/blob/master/schedule/__init__.py (run_continuously)
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def run_threaded(job_function):  # run every schedule on different threads
    job_thread = threading.Thread(target=job_function)
    job_thread.start()


def verify_price():
    curr_prices = get_all_prices_from_API()
    yesterday_prices = get_all_prices_from_API_for_date(search_date=datetime.today() - timedelta(days=1))

    print("verified euro for today= " + str(curr_prices[Currency.EURO]) + " & yesterday= " + str(yesterday_prices[Currency.EURO]))
    if abs(curr_prices[Currency.EURO] - yesterday_prices[Currency.EURO]) >= 0.2:
        send_message("wtf, man, euro is: " + str(curr_prices[Currency.EURO]) + ", just yesterday it was: " +
                     str(yesterday_prices[Currency.EURO]))

    print("verified dollar for today= " + str(curr_prices[Currency.US_DOLLAR]) + " & yesterday= " + str(yesterday_prices[Currency.US_DOLLAR]))
    if abs(curr_prices[Currency.US_DOLLAR] - yesterday_prices[Currency.US_DOLLAR]) >= 0.2:
        send_message("wtf, man, a dollar is: " + str(curr_prices[Currency.US_DOLLAR]) + ", just yesterday it was: " +
                     str(yesterday_prices[Currency.US_DOLLAR]))


def send_message(message: string):
    bot = telegram.Bot(token=BOT_TOKEN)
    bot.sendMessage(chat_id=CHAT_ID, text=message)
    print(message + " message sent")


def send_all_prices_message():
    curr_prices = get_all_prices_from_API()
    bot = telegram.Bot(token=BOT_TOKEN)
    try:
        bot.sendMessage(chat_id=CHAT_ID, text="1€ = " + str(curr_prices[Currency.EURO]) + "mdl, 1$ = " + str(
                                    curr_prices[Currency.US_DOLLAR]) + "mdl")
    except ConnectionError:
        bot.sendMessage(chat_id=CHAT_ID, text="Currency service unavailable")


def handle_start_command(update, context):
    print("handling command: /start")
    context.bot.sendMessage(chat_id=update.effective_chat.id, text="Available commands: /euro, /dollar, /all")


def handle_euro_command(update, context):
    print("handling command: /euro")
    try:
        context.bot.sendMessage(chat_id=update.effective_chat.id, text="1€ = " + str(get_price_from_API_for(Currency.EURO)) + "mdl")
    except ConnectionError:
        context.bot.sendMessage(chat_id=update.effective_chat.id, text="Currency service unavailable")


def handle_dollar_command(update, context):
    print("handling command: /dollar")
    try:
        context.bot.sendMessage(chat_id=update.effective_chat.id, text="1$ = " + str(get_price_from_API_for(Currency.US_DOLLAR)) + "mdl")
    except ConnectionError:
        context.bot.sendMessage(chat_id=update.effective_chat.id, text="Currency service unavailable")


def handle_all_command(update, context):
    print("handling command: /all")
    curr_prices = get_all_prices_from_API()
    try:
        context.bot.sendMessage(chat_id=update.effective_chat.id, text="1€ = " + str(curr_prices[Currency.EURO]) + "mdl, 1$ = " + str(curr_prices[Currency.US_DOLLAR]) + "mdl")
    except ConnectionError:
        context.bot.sendMessage(chat_id=update.effective_chat.id, text="Currency service unavailable")


def add_command_handler():
    updater = Updater(BOT_TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', handle_start_command))
    updater.dispatcher.add_handler(CommandHandler('euro', handle_euro_command))
    updater.dispatcher.add_handler(CommandHandler('dollar', handle_dollar_command))
    updater.dispatcher.add_handler(CommandHandler('all', handle_all_command))
    updater.start_polling()
    updater.idle()


schedule.every().hour.do(run_threaded, verify_price)
schedule.every().day.at('05:00').do(run_threaded, send_all_prices_message)  # every day at 08:00 UTC+3


if __name__ == '__main__':
    run_schedules_on_bg_thread()
    add_command_handler()
