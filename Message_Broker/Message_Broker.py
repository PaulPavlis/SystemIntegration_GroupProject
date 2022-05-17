import constants as keys
from telegram.ext import *
from activemq_publish_handler import send_message_2_queue
import json
import _thread
import time
from activemq_subscribe_handler import get_activemq_subscriber


def get_json_message_lamp(brightness=100, colour_hexa="FFFFFF", effect=""):
    return {
        "brightness": brightness,
        "colour_hexadecimal": colour_hexa,
        "special_effect": effect
    }


def get_send_details(user_message):
    destinations = "not_declared"
    json_message = "not_declared"
    telegram_answer = "not_declared"

    if user_message == "lamp1 on":
        destinations = ["/topic/topic_lamp1"]
        json_message = get_json_message_lamp(100, "FFFFFF", "")
        telegram_answer = "Sent command to lamp1."
    elif user_message == "lamp2 on":
        destinations = ["/topic/topic_lamp2"]
        json_message = get_json_message_lamp(100, "FFFFFF", "")
        telegram_answer = "Sent command to lamp2."
    elif user_message == "all_lamps on":
        destinations = ["/topic/topic_all_lamps"]
        json_message = get_json_message_lamp(100, "FFFFFF", "")
        telegram_answer = "Sent command to all lamps."
    else:
        return (None, None, None)

    return (destinations, json_message, telegram_answer)


def handle_message(update, context):
    user_message = str(update.message.text).lower()

    print(f"Received Telegram message: {user_message}")

    (destinations, json_message,
     telegram_answer) = get_send_details(user_message)

    if destinations is None:
        update.message.reply_text(
            "This is not a correct command. Type /help for more information.")
    else:
        update.message.reply_text(telegram_answer)
        for destination in destinations:
            json_string = json.dumps(json_message)
            send_message_2_queue(keys.HOST, keys.PORT,
                                 keys.USER, keys.PASSWORD, destination, json_string)
            print(f"Sent ActiveMQ message to {destination}: {json_string}")


def start_command(update, context):
    update.message.reply_text("Hello, I am the System Integration Bot")


def help_command(update, context):
    update.message.reply_text("No help for you ._.")


def error(update, context):
    print(f"Update {update} caused error {context.error}")


def keep_telegram_handler_open(updater, ):
    print("MessageBroker (Telegram Receiver) started ...")
    updater.start_polling(2)
    while 1:
        time.sleep(1)
    # updater.idle() # can't do this, because we are not in the main thread


def receive_activemq_messages(updater, ):

    # conn = get_activemq_subscriber(updater.message.reply_text)
    conn = get_activemq_subscriber(print)

    print("MessageBroker (ActiveMQ Receiver) started ...")
    while 1:
        time.sleep(1)


if __name__ == "__main__":
    updater = Updater(keys.TELEGRAM_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    try:
        _thread.start_new_thread(keep_telegram_handler_open, (updater, ))
        _thread.start_new_thread(receive_activemq_messages, (updater, ))
    except Exception as e:
        print(f"Error: Unable to start thread. Error message: {e}")

    # keep it forever open
    while 1:
        pass
