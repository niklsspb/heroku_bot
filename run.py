import logging
import sys
import os
from telegram.ext import *

from jobs import start, get_gold, get_everyday
from actions import get_my_orders


# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.DEBUG)
# logger = logging.getLogger(__name__)



def main(token):
    updater = Updater(token)
    jobs = updater.job_queue
    #jobs.run_repeating(sender_to_channel, 60)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("getgold", get_gold))
    dp.add_handler(CommandHandler("everyday", get_everyday))
    echo_handler = telegram.ext.MessageHandler(telegram.ext.Filters.text, get_my_orders)
    dp.add_handler(echo_handler)
    echo_handler2 = telegram.ext.MessageHandler(telegram.ext.Filters.group, get_my_orders)
    dp.add_handler(echo_handler2)
    #dp.add_handler(MessageHandler([Filters.text], get_my_orders))
    #dp.add_handler(MessageHandler([Filters.group], get_my_orders))
    # dp.add_handler(CallbackQueryHandler(router_callbacks))
    updater.start_polling(poll_interval=10.0)
    updater.idle()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main(os.getenv("TOKEN"))
