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

stones = {'перенос +1': '1',
          'перенос +2': '5',
          'перенос +3': '12',
          'перенос +4': '28',
          'перенос +5': '60',
          'перенос +6': '80',
          'перенос +7': '100',
          'перенос +8': '150',
          'перенос +9': '250',
          'перенос +10': '400',
          'перенос +11': '650',
          'перенос +12': '1000'
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
    try:
        image = g.doc.select(
            './/*[@id="public_wall"]/*[@id="page_wall_posts"]/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/a[@aria-label]/@onclick')[
            0].text()
        caption = 'Ежа'
        date_time = datetime.datetime.now()
        date_post = date_time.date()
        json_string = get_indexes(image)
        res = json.loads(json_string)
        result = res['temp']['y_']
        url_image = url + result[0] + '.jpg'
        return url_image
    except IndexError:
        return None


def get_course_gold():
    url = "https://pwcats.info/servers/scorpio"
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
    if len(reply_text) <= 12:
        chat_type = get_chat_type(update)
        if reply_text == "Кто по еже" or reply_text == "кто по еже" or reply_text == "ежа":
            if results is None:
                results = get_every_day()
                if results is not None:
                    if chat_type == "group":
                        bot.sendPhoto(chat_id=group_chat_id(update), photo=results,
                                      reply_to_message_id=update.message.message_id,
                                      caption=caption)
                    else:
                        bot.sendPhoto(chat_id=uid_from_update(update), photo=results,
                                      reply_to_message_id=update.message.message_id, caption=caption)
                else:
                    if chat_type == "group":
                        bot.sendMessage(chat_id=group_chat_id(update), text="Ошибка, повторите позже",
                                        reply_to_message_id=update.message.message_id,
                                        caption=caption)
                    else:
                        bot.sendMessage(chat_id=uid_from_update(update), text="Ошибка, повторите позже",
                                        reply_to_message_id=update.message.message_id, caption=caption)
            else:
                if chat_type == "group":
                    bot.sendPhoto(chat_id=group_chat_id(update), photo=results,
                                  reply_to_message_id=update.message.message_id,
                                  caption=caption)
                else:
                    bot.sendPhoto(chat_id=uid_from_update(update), photo=results,
                                  reply_to_message_id=update.message.message_id, caption=caption)
        if reply_text == "Голд" or reply_text == "голд":
            response = get_course_gold()
            if chat_type == "group":
                bot.sendMessage(chat_id=group_chat_id(update), text=response,
                                reply_to_message_id=update.message.message_id)
            else:
                bot.sendMessage(chat_id=uid_from_update(update), text=response,
                                reply_to_message_id=update.message.message_id)
        if reply_text.startswith("перенос") or reply_text.startswith("Перенос") or reply_text.startswith("ПЕРЕНОС"):
            result = stones.get(reply_text.lower())
            print(result)
            if chat_type == "group":
                bot.sendMessage(chat_id=group_chat_id(update), text='Нужно камней мироздания = ' + result,
                                reply_to_message_id=update.message.message_id)
            else:
                bot.sendMessage(chat_id=uid_from_update(update), text='Нужно камней мироздания = ' + result,
                                reply_to_message_id=update.message.message_id)
        if reply_text.lower() == 'пуха 30 па':
            response = calc_weapon_cost()
            if chat_type == "group":
                bot.sendMessage(chat_id=group_chat_id(update), text=response,
                                reply_to_message_id=update.message.message_id)
            else:
                bot.sendMessage(chat_id=uid_from_update(update), text=response,
                                reply_to_message_id=update.message.message_id)
        if reply_text.lower() == 'пуха 40 па':
            response = calc_weapon_cost_40_pa()
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


def calc_weapon_cost():
    """
    оружие на 30 па
    Требуется:
    400 - Кровавый камень
        1 кровавый камень крафтится из:
            1 фрагмента кровавого камня (небо), ID в котобазе 50249
            1 фрагмента кровавого камня (море), ID в котобазе 50251
    240 - Огненный камень
        1 огненный камень крафтится из:
            1 фрагмента огненного камня (небо), ID в котобазе 50255
            1 фрагмента огненного камня (море), ID в котобазе 50257
    120 - Небесная яшма
        крафтится из небесная яшма синяя, ID в котобазе 50259
    и 20кк
    """
    blood_stone = 400
    flame_stone = 240
    jasper = 120
    sum_blood_stone = calc(blood_stone, 50249) + calc(blood_stone, 50251)
    sum_flame_stone = calc(flame_stone, 50255) + calc(flame_stone, 50257)
    sum_jasper = calc(jasper, 50259)
    return str('Купить 400 Кровавых камней выйдет за сумму =' + str(
        sum_blood_stone) + '\n' + 'Купить 240 Огненных камней выйдет за сумму = ' + str(
        sum_flame_stone) + '\n' + 'Купить 120 небесной яшмы выйдет за сумму = ' + str(
        sum_jasper) + '\n' + 'За крафт пухи 20кк' + '\n' + 'Итого сумма = ' + str(
        int(sum_blood_stone) + int(sum_flame_stone) + int(sum_jasper) + 20000000))
    # return str(int(sum_blood_stone)+int(sum_flame_stone)+int(sum_jasper)+20000000)


def calc_weapon_cost_40_pa():
    """
    оружие на 30 па
    Требуется:
    400 - Кровавый камень
        1 кровавый камень крафтится из:
            1 фрагмента кровавого камня (небо), ID в котобазе 50249
            1 фрагмента кровавого камня (море), ID в котобазе 50251
    240 - Огненный камень
        1 огненный камень крафтится из:
            1 фрагмента огненного камня (небо), ID в котобазе 50255
            1 фрагмента огненного камня (море), ID в котобазе 50257
    120 - Небесная яшма
        крафтится из небесная яшма синяя, ID в котобазе 50259
    и 20кк
    """
    blood_stone = 1600
    flame_stone = 960
    jasper = 200
    trees = 70
    sum_blood_stone = calc(blood_stone, 50249) + calc(blood_stone, 50251)
    sum_flame_stone = calc(flame_stone, 50255) + calc(flame_stone, 50257)
    sum_jasper = calc(jasper, 50259)
    sum_tree = calc(trees, 50261)
    return str('Купить ' + blood_stone + ' Кровавых камней выйдет за сумму =' + str(
        sum_blood_stone) + '\n' + 'Купить ' + flame_stone + ' Огненных камней выйдет за сумму = ' + str(
        sum_flame_stone) + '\n' + 'Купить ' + jasper + ' небесной яшмы выйдет за сумму = ' + str(
        sum_jasper) + '\n' + 'Купить 70 Дерево еретика Линсю выйдет за сумму=' + str(
        sum_tree) + '\n' + 'За крафт пухи 50кк' + '\n' + 'Итого сумма = ' + str(
        int(sum_blood_stone) + int(sum_flame_stone) + int(sum_jasper) + int(sum_tree) + 50000000))
    # return str(int(sum_blood_stone)+int(sum_flame_stone)+int(sum_jasper)+20000000)


def calc(count, ID):
    url = "https://pwcats.info/scorpio"
    url = url + '/' + str(ID)
    g = Grab()
    g.go(url,
         user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 YaBrowser/17.11.1.990 Yowser/2.5 Safari/537.36')
    cost_list = g.doc.select('//*[@id = "sort_adw"]/tbody/tr[*]/td[5]/text()').node_list()
    for i in range(0, cost_list.__len__()):
        string = cost_list[i].replace(' ', '')
        cost_list[i] = int(string)
    # print(cost_list)
    print(min(cost_list))
    return min(cost_list) * count
