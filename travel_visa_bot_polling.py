
import sys
import telebot
from try_parsing_flags import write_data_flag_to_file, get_data_flag_in_file
from visa_parsing import write_data_visa_to_file, get_data_visa_in_file
from free_visa import write_data_free_visa_to_file, get_data_free_visa_in_file
from visa_tez_tour import read_covid_tez_in_file, write_covid_tez_to_file
import datetime
import pickle
from make_keyboard import make_keyboard
from try_cut_str_len import split_str
import config

TOKEN = config.bot_id
bot = telebot.TeleBot(TOKEN)

TG = None
counter_message = 0
my_id = 137336064

free_visa_dictionary_temp: dict
covid_list: list
free_visa_list: list
visa_list: list
all_countries_name: list
all_countries_name_lower: list
country: str
message_history = []
id_main_kb = None


def main():
    global TG, \
        counter_message, \
        my_id, \
        free_visa_dictionary_temp, \
        covid_list, \
        free_visa_list, \
        visa_list, \
        all_countries_name, \
        all_countries_name_lower, \
        country, \
        message_history, \
        id_main_kb

    collect_names_country_in_one_area('main')

    @bot.message_handler(commands=['start'])
    def start_user(message):
        global counter_message
        counter_message += 1
        delete_message(message, 0, counter_message, m_keyb=False)
        # send_notification_to_me(message)
        # write_user(message)
        text = f'Привет, {message.from_user.first_name}!\n' \
               f'Этот бот сможет сориентировать вас о требованиях других стран по правилам въезда по Covid-19\n\n' \
               f'Бот показывает информацию о правилах пересечения границ для беларусов.\n\n' \
               f'   - правила по Covid-19\n' \
               f'     (источник: https://www.tez-tour.com/)\n\n' \
               f'   - информация о визах, их стоимости, документах для подачи\n' \
               f'     (источник: https://vizoviyminsk.by/\n\n' \
               f'   - информация про безвизовые страны\n' \
               f'     (источник: https://tuda-suda.by/)\n\n' \
               f'Можно узнать информацию отдельно по:\n' \
               f'   - Covid ограничениям\n' \
               f'   - Визам (собраны страны в рубрике Виза)\n' \
               f'   - Безвизовым странам\n\n' \
               f'А также, в категории поиск по странам, можно узнать, кликнув на страну, ' \
               f'какие требования предъявляются ко всем, кто пересекает ее границу\n\n' \
               f'<b>/start</b> - перезапустить бот\n' \
            f'<b>/help</b> - получить информацию о боте\n' \
            f'<b>clear</b> - очистить окно бота от лишней информации при необходимости'
        bot.send_message(message.chat.id, text, disable_web_page_preview=True, parse_mode='html')
        main_keyboard(message)
        counter_message += 1

    @bot.message_handler(commands=['help'])
    def help_user(message):
        global counter_message
        counter_message += 1
        delete_message(message, 0, counter_message, m_keyb=False)
        text = \
            f'Этот бот сможет сориентировать вас о требованиях других стран по правилам въезда по Covid-19\n\n' \
            f'Бот показывает информацию о правилах пересечения границ для беларусов.\n\n' \
            f'   - правила по Covid-19\n' \
            f'     (источник: https://www.tez-tour.com/)\n\n' \
            f'   - информация о визах, их стоимости, документах для подачи\n' \
            f'     (источник: https://vizoviyminsk.by/\n\n' \
            f'   - информация про безвизовые страны\n' \
            f'     (источник: https://tuda-suda.by/)\n\n' \
            f'Можно узнать информацию отдельно по:\n' \
            f'   - Covid ограничениям\n' \
            f'   - Визам (собраны страны в рубрике Виза)\n' \
            f'   - Безвизовым странам\n\n' \
            f'А также, в категории поиск по странам, можно узнать, кликнув на страну, ' \
            f'какие требования предъявляются ко всем, кто пересекает ее границу\n\n' \
            f'<b>/start</b> - перезапустить бот\n' \
            f'<b>/help</b> - получить информацию о боте\n' \
            f'<b>clear</b> - очистить окно бота от лишней информации при необходимости'
        bot.send_message(message.chat.id, text, disable_web_page_preview=True, parse_mode='html')
        counter_message += 1

    @bot.message_handler(content_types=['text'])
    def catch_text(message):
        global \
            all_countries_name, \
            visa_list, \
            free_visa_list, \
            covid_list, \
            TG, \
            counter_message,\
            country, \
            all_countries_name_lower

        if message.text.lower() == 'clear':
            counter_message += 1
            clear_bot(message)

        if message.text.lower() == 'covid-19':
            counter_message += 1
            delete_message(message, 0, counter_message, m_keyb=True)
            covid_menu(message)

        if message.text.lower() == 'виза':
            TG = 'visa'
            counter_message += 1
            delete_message(message, 0, counter_message, m_keyb=True)
            visa_menu(message)

        if message.text.lower() == 'безвиз':
            TG = 'free_visa'
            counter_message += 1
            delete_message(message, 0, counter_message, m_keyb=True)
            free_visa_menu(message)

        if message.text.lower() == 'поиск по странам':
            TG = 'all_countries'
            counter_message += 1
            delete_message(message, 0, counter_message, m_keyb=True)
            all_countries_menu(message)

        if message.text.lower() == 'reload' and message.chat.id == 137336064:
            try:
                bot.send_message(
                    message.chat.id,
                    f"Обновление баз данных началась в {datetime.datetime.now().strftime('%H:%M %d-%m-%Y')}"
                )
                counter_message += 1

                fresh_all_data_to_files()
                bot.send_message(
                    message.chat.id,
                    f"Обновление баз данных прошла успешно {datetime.datetime.now().strftime('%H:%M %d-%m-%Y')}"
                )
                counter_message += 1

            except Exception as e:
                bot.send_message(message.chat.id, f'Обновления баз данных не произошло. Ошибка {e}')
                counter_message += 1

        if message.text.lower() == 'refresh' and message.chat.id == 137336064:
            try:
                bot.send_message(
                    message.chat.id,
                    f"Обновление переменных из баз началось в {datetime.datetime.now().strftime('%H:%M %d-%m-%Y')}"
                )
                counter_message += 1

                collect_names_country_in_one_area('refresh')
                bot.send_message(
                    message.chat.id,
                    f"Обновление переменных из баз прошла успешно {datetime.datetime.now().strftime('%H:%M %d-%m-%Y')}"
                )
                counter_message += 1
            except Exception as e:
                bot.send_message(message.chat.id, f'Обновление переменных из баз не прошло. Ошибка {e}')
                counter_message += 1

        if message.text.lower() == 'read users':
            counter_message += 1
            read_users(message)

        if message.text.lower() in all_countries_name_lower:
            counter_message += 1

            bot.send_message(message.chat.id, f'есть такая страна {message.text}')
            counter_message += 1

            collect_names_country_in_one_area('message text')
            country = all_countries_name[all_countries_name_lower.index(message.text.lower())]

            bot.send_message(message.chat.id, f'country = {country}')
            counter_message += 1

            # delete_message(message, 0, counter_message, m_keyb=False)
            send_all_countries_menu(message)
        else:
            counter_message += 1
            text = 'Возможно, по этой стране нет информации\n' \
                    'Вы можете воспользоваться меню внизу и выбрать страну из списка'
            if message.chat.id == my_id:
                if message.text.lower() not in ['clear', 'refresh', 'reload', 'read users', 'виза', 'безвиз', 'поиск по странам', 'covid-19']:
                    bot.send_message(message.chat.id, text)
                    counter_message += 1
            else:
                if message.text.lower() not in ['clear', 'виза', 'безвиз', 'поиск по странам', 'covid-19']:
                    bot.send_message(message.chat.id, text)
                    counter_message += 1

    @bot.callback_query_handler(func=lambda call: True)
    def send_inline(call):
        global \
            all_countries_name, \
            visa_list, \
            free_visa_list, \
            covid_list, \
            TG,\
            country, \
            counter_message

        if call.message:
            if call.data in ['продолжить',
                                 'Covid-19 в других странах',
                                 'безвиз в другие страны',
                                 'визы в другие страны']:

                match call.data:
                    case 'Covid-19 в других странах':
                        delete_message(call.message, 0, end=counter_message)
                        covid_menu(call.message)
                    case 'безвиз в другие страны':
                        delete_message(call.message, 0, end=counter_message)
                        free_visa_menu(call.message)
                    case 'визы в другие страны':
                        delete_message(call.message, 0, end=counter_message)
                        visa_menu(call.message)

            if call.data in all_countries_name and TG:
                country = call.data

            if call.data in all_countries_name and not TG:
                country = call.data
                send_all_countries_menu(call.message, call.data)

            if TG == 'covid':
                if call.data in covid_list:
                    covid_send_info(call.message, name_country=country, tagg=None)

            if TG == 'visa':
                if call.data in visa_list:
                    visa_send_info(call.message, name_country=country, tagg=None)

            if TG == 'free_visa':
                if call.data in free_visa_list:
                    free_visa_send_info(call.message, name_country=country, tagg=None)

            if TG == 'all_countries':
                send_all_countries_menu(call.message, call.data)

            if call.data == 'виза':
                counter_message += 1
                visa_send_info(call.message, name_country=country, tagg=None)

            if call.data == 'безвиз':
                counter_message += 1
                free_visa_send_info(call.message, name_country=country, tagg=None)

            if call.data == 'covid-19':
                counter_message += 1
                covid_send_info(call.message, tagg=None)


#  возвращает список из всех стран, собранных в разных информационных категориях с разных сайтов
def collect_names_country_in_one_area(text):
    global \
        all_countries_name, \
        visa_list, \
        free_visa_list, \
        covid_list, \
        free_visa_dictionary_temp, \
        all_countries_name_lower

    visa_dictionary = get_data_visa_in_file()
    free_visa_dictionary = get_data_free_visa_in_file()
    covid_dictionary = read_covid_tez_in_file()
    flags_dictionary = get_data_flag_in_file()

    visa_list = []
    for i in visa_dictionary:
        visa_list.append(i)

    free_visa_list_temp = []
    free_visa_dictionary_temp = {}

    free_visa_list = []
    for i in free_visa_dictionary:
        for j in free_visa_dictionary[i][0]:
            free_visa_list.append(j)
            free_visa_list_temp.append(j)
        free_visa_dictionary_temp[i] = list(filter(None, free_visa_list_temp))
        free_visa_list_temp = []
    free_visa_list = list(filter(None, free_visa_list))

    covid_list = []
    for i in covid_dictionary:
        covid_list.append(i)

    flags_list = []
    for i in flags_dictionary:
        flags_list.append(i)

    temp_countries: set
    temp_countries = set(visa_list).union(set(free_visa_list)).union(set(covid_list))
    temp_all_countries = list(temp_countries)
    temp_all_countries = list(filter(None, temp_all_countries))

    all_countries_name = []
    all_countries_name_lower = []

    while len(temp_all_countries):  # сортировка
        minim = min(temp_all_countries)
        if minim != 'Интересно о гербе Российская Федерация':
            all_countries_name.append(minim)
            all_countries_name_lower.append(minim.lower())
        temp_all_countries.pop(temp_all_countries.index(minim))

    print(text)

    return all_countries_name, visa_list, free_visa_list, covid_list, free_visa_dictionary_temp
    # список всех стран из всех категорий


def fresh_all_data_to_files():
    print(f"reload started at {datetime.datetime.now().strftime('%H:%M %d-%m-%Y')}")
    write_data_flag_to_file()
    write_data_visa_to_file()
    write_data_free_visa_to_file()
    write_covid_tez_to_file()
    write_data_free_visa_dict_to_file(collect_names_country_in_one_area('fresh')[4])
    print(f"reload finished at {datetime.datetime.now().strftime('%H:%M %d-%m-%Y')}")


def write_data_free_visa_dict_to_file(dictionary):
    sys.setrecursionlimit(10000)
    with open('data_free_visa_temp_dict.pickle', 'wb') as f:
        pickle.dump(dictionary, f)


def main_keyboard(message, text=f'Организуйте свой поиск в любой рубрике,\nлибо введите название страны на удачу'):
    global counter_message
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    it1 = telebot.types.KeyboardButton('Поиск по странам')
    it2 = telebot.types.KeyboardButton('Виза')
    it3 = telebot.types.KeyboardButton('Безвиз')
    it4 = telebot.types.KeyboardButton('Covid-19')
    markup.add(it1, it2, it3, it4)
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='html')
    counter_message += 1


def send_all_countries_menu(message):
    global country
    delete_message(message, 0, counter_message, m_keyb=False)
    buttons = []
    row: int
    if country in visa_list:
        buttons.append('виза')
    if country in covid_list:
        buttons.append('covid-19')
    if country in free_visa_list:
        buttons.append('безвиз')
    if len(buttons) < 3:
        row = 1
    else:
        row = 3
    inline_kb(message, country, buttons, send='send', rw=row, butt_down=True, tagg=None)


def visa_menu(message):
    global visa_list
    visa_list_name_countries = []
    text = f'При выборе страны в этом разделе, Вы получите информацию и визах, о названиях, ' \
           f'стоимости и необходимых документах для их получения\n' \
           f'Данные получены из ресурса https://vizoviyminsk.by/'

    for i in visa_list:
        visa_list_name_countries.append(i)
    inline_kb(message, text, visa_list_name_countries, 'send', rw=3, butt_down=True, tagg='visa')


def free_visa_menu(message):
    global free_visa_dictionary_temp, counter_message

    text = f'В этом разделе, при выборе страны из списка, вы сможете получить информацию какая виза нужна:\n' \
           f'   - виза через посольство или консульство\n' \
           f'   - виза по прилету\n' \
           f'   - онлайн виза\n' \
           f'а также информацию Covid-19 правилам пересечения границы страны\n' \
           f'Данные получены из ресурса https://tuda-suda.by/'
    bot.send_message(message.chat.id, text)
    counter_message += 1

    for key in free_visa_dictionary_temp:
        inline_kb(
            message,
            key.replace('<h2>', '').
            replace('</h2>', ''),
            free_visa_dictionary_temp[key],
            send='send',
            rw=3,
            butt_down=True,
            tagg='free_visa'
        )


def clear_bot(message):
    delete_message(message, 0, 15, m_keyb=False)
    main_keyboard(message)


def covid_menu(message):
    text = f'В этом разделе собрана информация по пересечению границ с некоторыми государствами в разрезе Covid-19\n' \
           f'Данные получены из ресурса https://www.tez-tour.com/\n\n' \
           f'Выберите страну, чтобы получить больше информации'
    inline_kb(message, text, covid_list, send='send', rw=3, butt_down=True, tagg='covid')


def all_countries_menu(message):
    global all_countries_name
    text = f'В этом разделе, при выборе страны из списка, вы сможете получить информацию какая виза нужна:\n' \
           f'   - виза через посольство или консульство\n' \
           f'   - виза по прилету\n' \
           f'   - онлайн виза\n' \
           f'а также информацию Covid-19 правилам пересечения границы страны'
    inline_kb(message, text, all_countries_name, send='send', rw=3, butt_down=True, tagg='all_countries')
    pass


def inline_kb(message, text, buttons: list, send='send', rw=3, butt_down=False, tagg=None):
    global TG, counter_message

    TG = tagg
    markup = telebot.types.InlineKeyboardMarkup(row_width=rw)

    if len(buttons) > 100:
        buttons_list = [buttons[0:99], buttons[99:]]

        markup = make_keyboard(message, markup, buttons_list[0], 3)
        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='html')
        counter_message += 1

        markup2 = telebot.types.InlineKeyboardMarkup(row_width=rw)
        make_keyboard(message, markup2, buttons_list[1], 3)
        bot.send_message(message.chat.id, 'еще:', reply_markup=markup2, parse_mode='html')
        counter_message += 1

    else:
        if rw == 3:
            make_keyboard(message, markup, buttons, rw)
        else:
            for i in buttons:
                markup.add(telebot.types.InlineKeyboardButton(i, callback_data=i))
        if len(text) <= 4096:
            bot.send_message(
                message.chat.id,
                text,
                reply_markup=markup,
                parse_mode='html',
                disable_web_page_preview=True
            )
            counter_message += 1
        else:
            text = split_str(text, 4096)
            i = 0
            while i < len(text)-1:
                bot.send_message(
                    message.chat.id,
                    text[i],
                    parse_mode='html',
                    disable_web_page_preview=True
                )
                i += 1
                counter_message += 1
            if not butt_down:
                bot.send_message(
                    message.chat.id,
                    text[i],
                    reply_markup=markup,
                    parse_mode='html',
                    disable_web_page_preview=True
                )
                counter_message += 1
            else:
                bot.send_message(
                    message.chat.id,
                    text[i],
                    parse_mode='html',
                    disable_web_page_preview=True
                )
                counter_message += 1


def delete_message(
        message,
        start=0,
        end=counter_message,
        m_keyb=True,
        text='Организуйте свой поиск в любой рубрике,\nлибо введите название страны на удачу'):

    global counter_message, TG

    if TG == 'free_visa':
        if message.text == 'Условно безвизовые страны для белорусов:':
            counter_message -= 1
            try:
                bot.delete_message(message.chat.id, message.message_id + 1)
            except Exception:
                pass
        elif message.text == 'Список безвизовых стран для белорусов 2022:':
            counter_message -= 2
            try:
                bot.delete_message(message.chat.id, message.message_id + 1)
                bot.delete_message(message.chat.id, message.message_id + 2)
            except Exception:
                pass

    if TG == 'all_countries':
        if message.text != 'ещё:':
            counter_message -= 1
            try:
                bot.delete_message(message.chat.id, message.message_id + 1)
            except Exception:
                pass

    for i in range(start, end):
        try:
            bot.delete_message(message.chat.id, message.message_id-i)
        except Exception:
            pass
    counter_message = 0

    if m_keyb == True:
        main_keyboard(message, text)


def visa_send_info(message, name_country, tagg=None):
    global counter_message

    visa_dictionary = get_data_visa_in_file()
    flags_dictionary = get_data_flag_in_file()

    delete_message(message, 0, counter_message,  m_keyb=True, text=f'{name_country}:\n\n<b>информация о визах</b>\nи условиях их получения')

    if name_country in flags_dictionary:
        try:
            bot.send_photo(message.chat.id, flags_dictionary[name_country])
        except Exception as e:
            print(f'флаг {name_country} не удалось отправить, ошибка {e}')
        counter_message += 1

    data = visa_dictionary[name_country]
    info = data[0]
    visa = data[1]
    count = 1
    data = f'{name_country}\n\n'

    if info:
        bot.send_message(message.chat.id, info)
        counter_message += 1

    for i in visa:
        for j in i:
            line = f"<b>{j if count>1 else f'<b>{data}</b>' + j}</b>\n" + i[j]
            if count < len(visa):
                bot.send_message(message.chat.id, line, parse_mode='html', disable_web_page_preview=True)
                counter_message += 1
            else:
                inline_kb(
                    message,
                    line,
                    ['визы в другие страны', name_country],
                    send='send',
                    rw=1,
                    butt_down=True,
                    tagg=tagg)
        count += 1


def free_visa_send_info(message, name_country, tagg=None):
    global counter_message

    delete_message(message, 0, 8,  m_keyb=True, text=f'<b>информация по безвизу</b>\n'
                                                     f'(визам по прилету, онлайн визам)')

    free_visa_dictionary = get_data_free_visa_in_file()
    flags_dictionary = get_data_flag_in_file()
    if name_country in flags_dictionary:
        try:
            bot.send_photo(message.chat.id, flags_dictionary[name_country])
        except Exception as e:
            print(f'флаг {name_country} не удалось отправить, ошибка {e}')
        counter_message += 1

    for i in free_visa_dictionary:
        temp = (free_visa_dictionary[i][0])
        free_text = ''
        if name_country in temp:
            match i:
                case 'Список безвизовых стран для белорусов 2022:':
                    free_text = f'\nБезвиз\n'
                case 'Условно безвизовые страны для белорусов:':
                    free_text = f'\nВиза по прилёту\n'
                case 'Другие условно безвизовые направления:':
                    free_text = f'\nОнлайн-виза\n'

            text = f'<b>{name_country}:</b>\n{free_text}\n{temp[name_country]}'
            inline_kb(
                message,
                text,
                ['безвиз в другие страны', name_country],
                send='send',
                rw=1,
                butt_down=True,
                tagg=tagg
            )
            break


def covid_send_info(message, tagg=None):
    global counter_message, country

    bot.send_message(message.chat.id, f'<b>country {country}</b>')

    covid_dictionary = read_covid_tez_in_file()
    flags_dictionary = get_data_flag_in_file()

    delete_message(message, 0, 5, m_keyb=True, text='<b>информация по Covid-19</b>')

    if country in flags_dictionary:
        try:
            bot.send_photo(message.chat.id, flags_dictionary[country])
        except Exception as e:
            print(f'флаг {country} не удалось отправить, ошибка {e}')
        counter_message += 1
    inline_kb(
        message,
        f'<b>{country}</b>\n\n{covid_dictionary[country]}',
        ['Covid-19 в других странах', country],
        send='send',
        rw=1,
        butt_down=False,
        tagg=tagg)



# def covid_send_info(message, name_country, tagg=None):
#     global counter_message
#
#     covid_dictionary = read_covid_tez_in_file()
#     flags_dictionary = get_data_flag_in_file()
#
#     delete_message(message, 0, 5, m_keyb=True, text='<b>информация по Covid-19</b>')
#
#     if name_country in flags_dictionary:
#         try:
#             bot.send_photo(message.chat.id, flags_dictionary[name_country])
#         except Exception as e:
#             print(f'флаг {name_country} не удалось отправить, ошибка {e}')
#         counter_message += 1
#     inline_kb(
#         message,
#         f'<b>{name_country}</b>\n\n{covid_dictionary[name_country]}',
#         ['Covid-19 в других странах', name_country],
#         send='send',
#         rw=1,
#         butt_down=False,
#         tagg=tagg)


def send_notification_to_me(message, text='Hi'):
    global counter_message, my_id
    text = f'user clicks /start:\n' \
           f'username = {message.from_user.username}\n' \
           f'first_name = {message.from_user.first_name}\n' \
           f'last_name = {message.from_user.last_name}\n' \
           f'chat_id = {message.chat.id}'
    bot.send_message(my_id, text)
    if message.chat.id == my_id:
        counter_message += 1


def write_user(message):
    flags = False

    with open('users_travel_bot.txt', 'r+') as f:

        if f.readline():
            for line in f:
                if line.split(';')[0] == message.from_user.username:
                    flags = True
                    break

            if flags == False:
                try:
                    f.writelines(
                        f"{message.from_user.username if str(message.from_user.username).isalnum() else 'not identified'};"
                        f"{message.from_user.first_name if str(message.from_user.first_name).isalnum() else 'not identified'};"
                        f"{message.from_user.last_name if str(message.from_user.last_name).isalnum() else 'not identified'};"
                        f"{message.chat.id};"
                        f"{datetime.datetime.now().strftime('%H:%M %d-%m-%Y')}\n"
                    )
                except Exception as e:
                    print('ошибка записи пользователя ', e)
        else:
            try:
                f.writelines(
                    f"{message.from_user.username if str(message.from_user.username).isalnum() else 'not identified'};"
                    f"{message.from_user.first_name if str(message.from_user.first_name).isalnum() else 'not identified'};"
                    f"{message.from_user.last_name if str(message.from_user.last_name).isalnum() else 'not identified'};"
                    f"{message.chat.id};"
                    f"{datetime.datetime.now().strftime('%H:%M %d-%m-%Y')}\n"
                )
            except Exception as e:
                print('ошибка записи пользователя ', e)


def read_users(message):
    global my_id
    text = ''
    with open('users_travel_bot.txt', 'r+') as f:
        for line in f:
            line_list = line.split(';')
            text = \
                text + \
                f'username: {line_list[0]}\n' \
                f'first_name: {line_list[1]}\n' \
                f'last_name: {line_list[2]}\n' \
                f'chat_id: {line_list[3]}\n' \
                f'date: {line_list[4]}\n\n'
        inline_kb(message, text, ['ok'], send='send', rw=1, butt_down=True)


# print('bot started')
# main()
# bot.polling()
