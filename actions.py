import datetime
import json
import logging

# import telegram
from grab import Grab

results = None
timestamp = datetime.datetime.now()
date = timestamp.date()
date_post = date
caption = None

dictionary = {'кх 1': 'Зал героев',
              'кх 2': 'Медная терраса для птиц',
              'кх 3': '30 ур.',
              'кх 4': 'Нет, нельзя. Можно заходить только на территорию своей базы',
              'кх 5': 'Очки личного вклада',
              'кх 6': 'Очки технологий',
              'кх 7': 'Такого показателя нет.',
              'кх 8': 'Очки технологий',
              'кх 9': 'Выполнять задания гильдии',
              'кх 10': 'Показатель станет равен нулю',
              'кх 11': 'Склад Жиангмен',
              'кх 12': 'Торговый городок',
              'кх 13': 'Зал героев',
              'кх 14': 'Аксессуары для свадебной церемонии',
              'кх 15': 'Особый камень очищения',
              'кх 16': 'Стихи',
              'кх 17': 'Таких зданий нет',
              'кх 18': 'Четвертого',
              'кх 19': 'Восьмого',
              'кх 20': 'Стихи пределов',
              'кх 21': 'Благословение усиления',
              'кх 22': 'Камень грез',
              'кх 23': 'Песок погребения',
              'кх 24': 'Да',
              'кх 25': 'Выполняя задания гильдии, материалы получить нельзя',
              'кх 26': 'Такого показателя нет',
              'кх 27': 'Только мастер гильдии может уничтожать постройки',
              'кх 28': 'Постройки гильдии не могут быть уничтожены в войне гильдий',
              'кх 29': 'Такого показателя нет',
              'кх 30': 'Да',
              'кх 31': 'Право выбирать постройки для улучшения',
              'кх 32': 'Вклад участников гильдии',
              'кх 33': 'Да',
              'кх 34': 'Саблю для фехтования',
              'кх 35': 'Древние',
              'кх 36': 'В одна тысяча сорок четвертом',
              'кх 37': 'Золотая маска',
              'кх 38': 'Обитель ужаса',
              'кх 39': 'Сон в красном тереме',
              'кх 40': 'Опыт',
              'кх 41': 'Нападающие могут разорить запасы замка',
              'кх 42': 'Генерал армии тигров-оборотней',
              'кх 43': 'Администратор базы гильдии',
              'кх 44': 'Каменное перо',
              'кх 45': 'На нем поселились призраки',
              'кх 46': 'В ущелье Шэнь У',
              'кх 47': 'Неизменный город',
              'кх 48': 'Пять',
              'кх 49': 'Третьим глазом',
              'кх 50': 'Хей Яо',
              'кх 51': 'Великий источник',
              'кх 52': 'Александр',
              'кх 53': 'Элмсли',
              'кх 54': 'Долина расхитителей небес',
              'кх 55': 'В Город боевых песен вторглась армия Кровавого Ло',
              'кх 56': 'Печальный дух Джейд',
              'кх 57': 'Великий маг Тэнг',
              'кх 58': 'Колесо времени',
              'кх 59': 'Сиды',
              'кх 60': 'В пределе дьявольских наваждений',
              'кх 61': 'Нет, нельзя. Можно заходить только на территорию своей базы',
              'кх 62': 'Для победы нужно разрушить базу противника',
              'кх 63': 'С последователем Шэнь Инь',
              'кх 64': 'Война гильдий длится определенное время',
              'кх 65': 'Песок преображения',
              'кх 66': '6',
              'кх 67': 'Зал отдыха',
              'кх 68': 'С варварами',
              'кх 69': 'Чтобы разгадать тайну долины',
              'кх 70': 'Город Инея'
              }

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_chat_type(update):
    chat_type = None
    try:
        chat_type = update.message.chat.type
    except (NameError, AttributeError):
        pass
    return chat_type


def get_data(update):
    callback_data_text = None
    try:
        callback_data_text = update.callback_query.data
        print(callback_data_text)
    except (NameError, AttributeError):
        logging.error("Not set")
    return callback_data_text


def get_user(update):
    username = None
    try:
        username = update.callback_query.from_user.first_name + " " + update.callback_query.from_user.last_name
    except (NameError, AttributeError):
        logging.error("Не удалось получить имя пользователя")
    return username


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


def get_course_gold():
    url = "https://pwcats.info/servers/drakon"
    g = Grab()
    g.go(url, user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/62.0.3202.94 '
                         'YaBrowser/17.11.1.990 Yowser/2.5 Safari/537.36')
    pay_list = g.doc.select('/html/body/div[1]/div/div/div[2]/aside/table[1]/tbody/tr[*]/td[1]/text()').node_list()
    sale_list = g.doc.select('/html/body/div[1]/div/div/div[2]/aside/table[1]/tbody/tr[*]/td[2]/text()').node_list()
    # print(pay_list[0])
    # print(pay_list[0].replace(' ', ''))
    for i in range(0, pay_list.__len__()):
        string = pay_list[i].replace(' ', '')
        string = string.replace('\n', '')
        index = string.find('(')
        pay_list[i] = string[0:index]
    for i in range(0, sale_list.__len__()):
        str_sale = sale_list[i].replace(' ', '')
        str_sale = str_sale.replace('\n', '')
        index = str_sale.find('(')
        sale_list[i] = str_sale[0:index]
    return "Продают по " + min(pay_list) + '\nCкупают по ' + max(sale_list)


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


def get_indexes(string):
    start_index = string.find('{')
    end_index = string.find('}')
    return string[start_index:end_index + 1] + '}'


def group_chat_id(update):
    group_chat_i_d = None
    try:
        group_chat_i_d = update.message.chat.id
    except (NameError, AttributeError):
        pass
    return group_chat_i_d


def get_my_orders(bot, update):
    global caption
    global results
    check_date()
    reply_text = update.message.text
    if len(reply_text) <= 10:
        chat_type = get_chat_type(update)
        if reply_text == "Кто по еже" or reply_text == "кто по еже" or reply_text == "ежа":
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
        if reply_text.startswith("кх") or reply_text.startswith("Кх") or reply_text.startswith("КХ"):
            result = dictionary.get(reply_text.lower())
            if chat_type == "group":
                bot.sendMessage(chat_id=group_chat_id(update), text=result,
                                reply_to_message_id=update.message.message_id)
            else:
                bot.sendMessage(chat_id=uid_from_update(update), text=result,
                                reply_to_message_id=update.message.message_id)
        if reply_text == "Голд" or reply_text == "голд":
            response = get_course_gold()
            if chat_type == "group":
                bot.sendMessage(chat_id=group_chat_id(update), text=response,
                                reply_to_message_id=update.message.message_id)
            else:
                bot.sendMessage(chat_id=uid_from_update(update), text=response,
                                reply_to_message_id=update.message.message_id)

    else:
        pass
    # else:
    #     # регулярное выражение для задания места работы сотрудника
    #     pattern = re.compile("^(\D{0,}),(\D{0,})$")
    #     match = pattern.match(reply_text)
    #     city = match.group(1).strip()
    #     shop = match.group(2).strip()
    #     search_shops(bot, city, shop, update)


def get_message_id(updater):
    message_i_d = None
    try:
        message_i_d = updater.callback_query.message_id
    except (NameError, AttributeError):
        try:
            message_i_d = updater.callback_query.message.message_id
            print(message_i_d)
        except (NameError, AttributeError):
            logging.error("Не удалось получить message_i_d")
    return message_i_d


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
