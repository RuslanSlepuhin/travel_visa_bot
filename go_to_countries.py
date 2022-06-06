
import requests
from bs4 import BeautifulSoup
import re
import telebot
from try_parsing_flags import get_link_flag
from try_cut_str_len import split_str
from visa_parsing import get_url_countries, get_info_visa
import datetime
from bezvis import get_info_bszvis, list_countries
from make_keyboard import make_keyboard

TG = 'covid'
c_data = ''
all_countries = []

# bot = telebot.TeleBot('5386299618:AAH38RyA8zHwbkT8zMPINkJiYf76oUvgkZs')

HOST = 'https://belavia.by/'
URL = 'https://belavia.by/covid_informatsiya_po_ogranicheniyu/'
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
}
rules: list


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    global rules
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='accordion-pane')
    rules = []

    for it in items:
        rules.append(
            {
                'country': str(it.find('p', class_='t-h2').find('a').get_text()),
                'text': text_format(str(it.find('div', class_='accordion-description')))
            }
        )
    return rules


def text_format(text):
    text = text.replace('<div class="accordion-description">', '')
    text = text.replace('</div>', '')
    text = text.replace('<div>', '')
    text = text.replace('<li>', '')
    text = text.replace('</li>', '')
    text = text.replace('<p>', '')
    text = text.replace('</p>', '')
    text = text.replace('<ul>', '')
    text = text.replace('</ul>', '')
    text = text.replace('</ol>', '')
    text = text.replace('<ol>', '')
    text = text.replace('<b3>', '')
    text = text.replace('</b3>', '')
    text = text.replace('<h3>', '')
    text = text.replace('</h3>', '')
    text = text.replace('<br/>', '')
    text = text.replace('</br>', '')
    text = text.replace('<br>', '')
    text = text.replace('</u>', '')
    text = text.replace('<u>', '')
    text = text.replace('</strong>', '')
    text = text.replace('<strong>', '')

    text = re.sub(r'\n{2,}', '\n', text)

    return text


# @bot.message_handler(commands=['start'])
# def start(message):
#     countries: list = []
#     for cy in rules:
#         countries.append(cy['country'])
#     text = f'Привет, {message.from_user.first_name}!\n' \
#            f'Этот бот сможет сориентировать вас о требованиях других стран по правилам въезда по Covid-19\n\n' \
#            f'Бот показывает информацию о правилах пересечения границ для беларусов.\n\n' \
#            f'   - правила по Covid-19\n' \
#            f'     (источник: https://belavia.by/)\n\n' \
#            f'   - информация о визах, их стоимости, документах для подачи\n' \
#            f'     (источник: https://vizoviyminsk.by/\n\n' \
#            f'   - информация про безвизовые страны\n' \
#            f'     (источник: https://tuda-suda.by/)'
#     bot.send_message(message.chat.id, text, parse_mode='html')
#     main_keyboard(message)
#
#
# @bot.message_handler(commands=['help'])
# def help(message):
#     text = \
#         f'Этот бот показывает информацию о правилах пересечения границ для беларусов.\n\n' \
#         f'   - правила по Covid-19\n' \
#         f'     (источник: https://belavia.by)\n\n' \
#         f'   - информация о визах, их стоимости, документах для подачи\n' \
#         f'     (источник: https://vizoviyminsk.by/\n\n' \
#         f'   - информация про безвизовые страны\n' \
#         f'     (источник: https://tuda-suda.by/)'
#
#     bot.send_message(message.chat.id, text, parse_mode='html')
#
#
# def main_keyboard(message, text='Выберите раздел'):
#     markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
#     it1 = telebot.types.KeyboardButton('Covid-19')
#     it2 = telebot.types.KeyboardButton('Visa')
#     it3 = telebot.types.KeyboardButton('Безвиз')
#     it4 = telebot.types.KeyboardButton('Поиск по странам')
#     markup.add(it1, it2, it3, it4)
#     bot.send_message(message.chat.id, text, reply_markup=markup)
#
#
# def inline_covid(message):
#     global rules
#     inline_kb(
#         message,
#         [i['country'] for i in rules],
#         f'В этом разделе собрана информация по пересечению границ с некоторыми государствами в разрезе Covid-19\n'
#         f'Данные с сайта belavia.by\n\n'
#         f'Выберите страну, чтобы получить больше информации',
#         tg='covid')
#
# def inline_bezvis(message):
#     text = \
#         f'В этом разделе страны, по которым:\n' \
#         f'   - действует безвиз,\n' \
#         f'   - визы по прилёту\n' \
#         f'   - электронные визы\n\n' \
#         f'Выберите страну, чтобы получить больше информации'
#     inline_kb(message, list_countries(get_info_bszvis()), [text], 'free_visa')
#
#
# def inline_visa(message):
#     inline_kb(message, get_url_countries(),
#               f'В этом разделе собраны страны, куда нужна виза для беларусов\n'
#               f'Данные с сайта визового центра vizoviyminsk.by\n'
#               f'Стоимость в конце сообщения - это стоимость визового центра по оформлению визы\n\n'
#               f'Выберите страну, чтобы получить больше информации',
#               tg='visa')
#
#
# def inline_search_from_countries(message):
#     all_countries = set(list_countries(get_info_bszvis())).union(set(get_url_countries()))
#     all_countries_list = []
#     all_countries = list(all_countries)
#     while all_countries:
#         i = min(all_countries)
#         all_countries_list.append(i)
#         all_countries.pop(all_countries.index(i))
#
#     print('all_countries = ', all_countries_list[0:-1])
#     text = f'В этом разделе собрано много стран из разных источников.\n' \
#            f'Вы можете открыть любую из них, чтобы понять:\n' \
#            f'   -нужна ли виза\n' \
#            f'   -либо для этой страны действует безвиз, либо электронная, либо виза по прилету\n' \
#            f'   -требования по Covid-19 (не для всех стран есть информация ' \
#            f'из-за ограниченного списка стран на сайте belavia.by)'
#     inline_kb(message, all_countries_list[0:-1], text, tg='from_countries')
#
#
# @bot.message_handler(content_types=['text'])
# def some_text(message):
#     global rules, all_countries
#
#     if message.text == 'Covid-19':
#         inline_covid(message)
#
#     elif message.text == 'Visa':
#         inline_visa(message)
#
#     elif message.text == 'Безвиз':
#         inline_visa(message)
#
#     elif message.text == 'Поиск по странам':
#         inline_search_from_countries(message)
#
#
# def inline_kb(message, buttons, text, tg='covid', row_w=3, butt_down=False):
#
#     global TG
#     TG = tg
#     dictionary: dict = {}
#
#     for i in range(0, len(buttons)):
#         dictionary[i] = buttons[i]
#
#     markup = telebot.types.InlineKeyboardMarkup(row_width=4)
#     if row_w == 3:
#         make_keyboard(message, markup, dictionary, row_w)
#     else:
#         for i in dictionary:
#             markup.add(telebot.types.InlineKeyboardButton(dictionary[i], callback_data=dictionary[i]))
#
#     if len(text) <= 4096:
#         bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='html')
#     else:
#         text = split_str(text, 4096)
#         i = 0
#         while i < len(text)-1:
#             bot.send_message(message.chat.id, text[i], parse_mode='html')
#             i += 1
#         if not butt_down:
#             bot.send_message(message.chat.id, text[i], reply_markup=markup, parse_mode='html')
#         else:
#             bot.send_message(message.chat.id, text[i], parse_mode='html')
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def send_inline(call):
#     global rules, TG, c_data, all_countries
#
#     if call.message:
#         if call.data:
#             if TG == 'covid':
#                 print_info_covid(call.message, call.data)
#
#             if TG == 'visa':
#                 print_info_visa(call.message, call.data)
#
#             buttons = []
#             if TG == 'from_countries' and call.data not in all_countries[0:-1]:
#                 c_data = call.data
#                 print(c_data)
#                 if call.data in list_countries(get_info_bszvis()):
#                     buttons.append('Безвиз')
#                 if call.data in get_url_countries():
#                     buttons.append('Visa')
#                 if call.data in [i['country'] for i in rules]:
#                     buttons.append('Covid-19')
#                 inline_kb(call.message, buttons, f'{call.data}', tg='choise_countries', row_w=1)
#
#             if TG == 'choise_countries':
#                 print('c_data ', c_data)
#                 print('call.data ', call.data)
#                 c = c_data
#                 if call.data == 'Безвиз':
#                     print(call.message.text)
#                     print_info_free_visa(call.message, call.message.text)
#                 elif call.data == 'Visa':
#                     print(call.message.text)
#                     print_info_visa(call.message, call.message.text)
#                 elif call.data == 'Covid-19':
#                     print_info_covid(call.message, call.message.text)
#
#             if call.data == 'продолжить в разделе поиска по странам':
#                 inline_search_from_countries(call.message)
#
#             if call.data == 'продолжить в разделе Безвиз':
#                 inline_bezvis(call.message)
#
#             if call.data == 'продолжить в разделе Визы':
#                 inline_visa(call.message)
#
#             if call.data == 'продолжить в разделе Covid-19':
#                 inline_covid(call.message)
#
#
# def print_info_free_visa(message, country):
#     get_info_bszvis(country)
#     for i in get_info_bszvis():
#         if i.split('\n')[0] == country:
#             print(i)
#             try:
#                 bot.send_photo(message.chat.id, get_link_flag(country)[0]['flag_link'])
#             except Exception as e:
#                 print(f'Flag not found (Error: {e})')
#             inline_kb(message, ['продолжить в разделе Безвиз'], i, 'free_visa', row_w=1)
#
#
# def print_info_visa(message, country):
#     global TG
#     try:
#         bot.send_photo(message.chat.id, get_link_flag(country)[0]['flag_link'], parse_mode='html')
#     except Exception as e:
#         print('Error 152 ', e)
#     line = f'<b>{country}</b>\n\n'
#     info_visa = get_info_visa(country)
#     count = 1
#     for i in info_visa:
#         for j in i:
#             if j == 'name_visa':
#                 line = line + f'<b>{i[j]}</b>' + f'\n'
#             else:
#                 line = line + i[j] + f'\n'
#         if count < len(info_visa):
#             bot.send_message(message.chat.id, line, parse_mode='html')
#             count += 1
#         else:
#             # inline_kb(message, ['продолжить в разделе Визы'], line, 'visa', row_w=1)
#             bot.send_message(message.chat.id, line, parse_mode='html')
#
#         line = ''
#
#
# def print_info_covid(message, country):
#     global TG
#     for i in rules:
#         if i.get('country') == country:
#             try:
#                 bot.send_photo(message.chat.id, get_link_flag(country)[0]['flag_link'])
#             except Exception as e:
#                 print(f'Flag not found (Error: {e})')
#
#             inline_kb(message, ['продолжить в разделе Covid-19'], f"<b>{i['country']}</b>\n{i['text']}", 'covid', row_w=1)
#

def get_covid_dictionary():
    global rules
    return rules


# print(f"bot started at {datetime.datetime.now().strftime('%H:%M %d-%m-%Y')}")
html = get_html(URL)
rules = get_content(html.text)
get_covid_dictionary()


# bot.polling()
