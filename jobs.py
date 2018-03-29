import datetime
import json
import logging

from grab import Grab

from actions import get_course_gold, get_chat_type, get_indexes, group_chat_id

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.DEBUG)
# logger = logging.getLogger(__name__)

results = None
timestamp = datetime.datetime.now()
date = timestamp.date()
date_post = date
caption = None


def check_date():
    global results
    global date_post
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.date()
    if date_post is not None:
        # noinspection PyTypeChecker
        if date_post < current_date:
            results = None
            date_post = None
    else:
        pass
		

def get_every_day():
    global caption
    global date_post
    url = "https://pp.userapi.com/"
    g = Grab()
    g.go("https://vk.com/dragpw",
         user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 '
                    'YaBrowser/17.11.1.990 Yowser/2.5 Safari/537.36')
    # list = g.doc.body.decode('cp1251')
    image = g.doc.select('.//*[@id="wall_fixed"]/div/div/div/div/div[2]/div/div/div/div[2]/a/@onclick')[0].text()
    caption = g.doc.select('.//*[@id="wall_fixed"]/div/div/div/div/div[2]/div/div/div/div[1]')[0].text()
    date_time = datetime.datetime.now()
    date_post = date_time.date()
    json_string = get_indexes(image)
    res = json.loads(json_string)
    result = res['temp']['y_']
    url_image = url + result[0] + '.jpg'
    return url_image


def uid_from_update(update):
    """
   Extract the chat id from update
   :param update: `telegram.Update`
   :return: chat_id extracted from the update
   """
    chat_id = None
    try:
        chat_id = update.message.from_user.id
    except (NameError, AttributeError):
        try:
            chat_id = update.inline_query.from_user.id
        except (NameError, AttributeError):
            try:
                chat_id = update.chosen_inline_result.from_user.id
            except (NameError, AttributeError):
                try:
                    chat_id = update.callback_query.from_user.id
                except (NameError, AttributeError):
                    logging.error("No chat_id available in update.")
    return chat_id


def start(bot, update):
    chat_id = uid_from_update(update)
    bot.sendMessage(chat_id=chat_id, text="Приветули")


def get_gold(bot, update):
    chat_type = get_chat_type(update)
    response = get_course_gold()
    if chat_type == "group":
        bot.sendMessage(chat_id=group_chat_id(update), text=response,
                        reply_to_message_id=update.message.message_id)
    else:
        bot.sendMessage(chat_id=uid_from_update(update), text=response,
                        reply_to_message_id=update.message.message_id)


def get_everyday(bot, update):
    global results
    check_date()
    chat_type = get_chat_type(update)
    if results is None:
        results = get_every_day()
        if chat_type == "group":
            bot.sendPhoto(chat_id=group_chat_id(update), photo=results,
                          reply_to_message_id=update.message.message_id,
                          caption=caption)
        else:
            bot.sendPhoto(chat_id=uid_from_update(update), photo=results,
                          reply_to_message_id=update.message.message_id, caption=caption)
    else:
        if chat_type == "group":
            bot.sendPhoto(chat_id=group_chat_id(update), photo=results,
                          reply_to_message_id=update.message.message_id,
                          caption=caption)
        else:
            bot.sendPhoto(chat_id=uid_from_update(update), photo=results,
                          reply_to_message_id=update.message.message_id, caption=caption)
