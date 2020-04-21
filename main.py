import threading  # run multiple schedules at once
import schedule  # update the currency data without command
import time  # sleep() after running schedule in while True

import telegram  # send messages
from telegram.ext import Updater, CommandHandler  # handle commands

import requests  # fetch data from currency API
import json  # read data from API response

import string


API_LINK = "https://free.currconv.com/api/v7/convert?q=EUR_MDL&compact=ultra&apiKey=446a1c3f6ca25a4c2315"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

BOT_TOKEN = 
CHAT_ID =


def run_schedules_on_bg_thread(interval=1):

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


def get_euro_price_from_API() -> float:  # TODO: add error handling
    api_response = requests.get(API_LINK, headers=HEADERS)
    currency = json.loads(api_response.content)
    return round(currency["EUR_MDL"], 2)


def verify_price():
    curr = get_euro_price_from_API()
    if curr >= 20 or curr <= 19:
        send_message("Pizdetz, schimba leii, euro costa: " + curr)


def send_message(message: string):
    bot = telegram.Bot(token=BOT_TOKEN)
    bot.sendMessage(chat_id=CHAT_ID, text=message)
    print(message + " message sent")


def send_euro_price_message():  # don't know how to pass send_message()'s arguments in add_handler()
    send_message(get_euro_price_from_API())


def send_message_bot(update, context):  # signature needed for telegram API
    print("handling command: /euro")
    context.bot.sendMessage(chat_id=update.effective_chat.id, text=get_euro_price_from_API())


def add_command_handler():
    updater = Updater(BOT_TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('euro', send_message_bot))
    updater.start_polling()
    updater.idle()


schedule.every().hour.do(run_threaded, verify_price)
schedule.every().day.at('05:00').do(run_threaded, send_euro_price_message)  # every day at 08:00 UTC+3


if __name__ == '__main__':
    run_schedules_on_bg_thread()
    add_command_handler()
