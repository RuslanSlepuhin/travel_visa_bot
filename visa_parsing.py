
import requests
from bs4 import BeautifulSoup
import re
import pickle

URL_DICT = {
    'Индия': 'https://vizoviyminsk.by/vizy-v-strany-azii/indiya/',
    'Польша': 'https://vizoviyminsk.by/viza-shengen/polsha/',
    'Литва': 'https://vizoviyminsk.by/viza-shengen/litva/',
    'Испания': 'https://vizoviyminsk.by/viza-shengen/ispaniya/',
    'Франция': 'https://vizoviyminsk.by/viza-shengen/franciya/',
    'Италия': 'https://vizoviyminsk.by/viza-shengen/italiya/',
    'Греция': 'https://vizoviyminsk.by/viza-shengen/greciya',
    'Бельгия': 'https://vizoviyminsk.by/viza-shengen/belgiya',
    'Венгрия': 'https://vizoviyminsk.by/viza-shengen/vengriya',
    'Латвия': 'https://vizoviyminsk.by/viza-shengen/latviya',
    'Дания': 'https://vizoviyminsk.by/viza-shengen/daniya',
    'Германия': 'https://vizoviyminsk.by/viza-shengen/germaniya',
    'Нидерланды': 'https://vizoviyminsk.by/viza-shengen/niderlandy',
    'Норвегия': 'https://vizoviyminsk.by/viza-shengen/norvegiya',
    'Португалия': 'https://vizoviyminsk.by/viza-shengen/portugaliya',
    'Словакия': 'https://vizoviyminsk.by/viza-shengen/slovakiya',
    'Словения': 'https://vizoviyminsk.by/viza-shengen/sloveniya',
    'Финляндия': 'https://vizoviyminsk.by/viza-shengen/finlyandiya',
    'Эстония': 'https://vizoviyminsk.by/viza-shengen/ehstoniya',
    'Швеция': 'https://vizoviyminsk.by/viza-shengen/shveciya',
    'Чехия': 'https://vizoviyminsk.by/viza-shengen/chekhiya',
    'Австрия': 'https://vizoviyminsk.by/viza-shengen/avstriya',
    'Исландия': 'https://vizoviyminsk.by/viza-shengen/islandiya',
    'Южная Корея': 'https://vizoviyminsk.by/vizy-v-strany-azii/yuzhnaya-koreya',
    'Япония': 'https://vizoviyminsk.by/vizy-v-strany-azii/yaponiya',
    'Китай': 'https://vizoviyminsk.by/vizy-v-strany-azii/kitaj',
    'Сингапур': 'https://vizoviyminsk.by/vizy-v-strany-azii/singapur',
    'Таиланд': 'https://vizoviyminsk.by/vizy-v-strany-azii/tailand',
    'Гонгконг': 'https://vizoviyminsk.by/vizy-v-strany-azii/gonkong',
    'Бангладеш': 'https://vizoviyminsk.by/vizy-v-strany-azii/bangladesh',
    'Бахрейн': 'https://vizoviyminsk.by/vizy-v-strany-azii/bakhrejn',
    'Мьянма': 'https://vizoviyminsk.by/vizy-v-strany-azii/myanma',
    'Тайвань': 'https://vizoviyminsk.by/vizy-v-strany-azii/tajvan',
    'Великобритания': 'https://vizoviyminsk.by/vizy/velikobritaniya',
    'Австралия': 'https://vizoviyminsk.by/vizy/avstraliya',
    'Мексика': 'https://vizoviyminsk.by/vizy/meksika',
    'Ирландия': 'https://vizoviyminsk.by/vizy/irlandiya',
    'Кипр': 'https://vizoviyminsk.by/vizy/kipr',
    'Канада': 'https://vizoviyminsk.by/vizy/kanada',
    'Болгария': 'https://vizoviyminsk.by/vizy/bolgariya',
    'Марокко': 'https://vizoviyminsk.by/vizy/marokko',
    'ЮАР': 'https://vizoviyminsk.by/vizy/yuar',
    'Доминикана': 'https://vizoviyminsk.by/vizy/dominikana',
    'Индонезия': 'https://vizoviyminsk.by/vizy/indoneziya',
    'Колумбия': 'https://vizoviyminsk.by/vizy/kolumbia',
    'Зимбабве': 'https://vizoviyminsk.by/vizy/zimbabve',
    'Египет': 'https://vizoviyminsk.by/vizy/egipet',
    'Алжир': 'https://vizoviyminsk.by/vizy/alzhir',
    'Кения': 'https://vizoviyminsk.by/vizy/keniya',
    'Мозамбик': 'https://vizoviyminsk.by/vizy/mozambik',
    'Сенегал': 'https://vizoviyminsk.by/vizy/senegal',
    'Остров Реюньон': 'https://vizoviyminsk.by/vizy/ostrov-reyunon',
    'Новая Зеландия': 'https://vizoviyminsk.by/vizy/novuyu-zelandiya',
    'Оман': 'https://vizoviyminsk.by/vizy/oman'
}

HOST = 'https://vizoviyminsk.by//'
URL = 'https://vizoviyminsk.by/vizy-v-strany-azii/indiya/'

HEADERS = {
    "accept":
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
        'application/signed-exchange;v=b3;q=0.9',
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/101.0.4951.67 Safari/537.36'
}

visa_dict: dict


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def clear_text(text):
    return re.sub(r'\n{2,}', '\n', text)


def get_url_countries():  # возвращает список стран, по которым есть информация по визам
    url_list = list(URL_DICT.keys())
    return url_list


# возвращает глобальный словарь со странами и urlами на получение от сайта информации (на разных страницах каждая страна
def get_url_visa_country():
    return URL_DICT


def get_info_visa():  # информация о визах по названию страны в запросе
    global URL_DICT
    global visa_dict
    visa_dict = {}

    for name_country in URL_DICT:

        html = get_html(URL_DICT[name_country])
        soup = BeautifulSoup(html.text, 'html.parser')
        block2 = soup.find_all('div', class_='row py-3 my-2 mx-0')

        temp_name_list = []
        temp_info_list = []
        temp_info_preview = []

        for i in block2:
            name = ''
            name1 = ''
            name2 = ''
            name3 = ''
            name4 = ''
            info1 = ''
            info2 = ''
            try:
                name = clear_text(i.find('div', class_='col-12 p-0').find('h4', class_='ml-lg-1').text)
            except Exception:
                pass
            try:
                name1 = clear_text(i.find('div', class_='col-12 p-0').find('p').find('span').text)
            except Exception:
                pass

            try:
                name2 = clear_text(i.find('div', class_="row mx-1 py-3").text)
            except Exception:
                pass

            try:
                name3 = clear_text(i.find('div', class_='mx-1 mt-3 border p-3').find('span', class_='h4').text)
            except Exception:
                pass

            try:
                name4 = clear_text(i.find('div', class_='mx-1 mt-3 border p-3').find('ul').text)
            except Exception:
                pass

            try:
                info1 = clear_text(i.find('div', class_='col-12 p-0').find('p', class_='ml-lg-1').text)
            except Exception:
                pass

            try:
                info2 = clear_text(i.find('div', class_='col-12 p-0').find('div', class_='col-12').find('ul').text)
            except Exception:
                pass

            if name:
                temp_name_list.append({name: name1 + name2 + name3 + name4})
            if info1 or info2:
                temp_info_list.append(info1 + info2)
            if name2 and not name:
                temp_info_preview.append(name2)

        visa_dict[name_country] = [temp_info_preview, temp_name_list, temp_info_list]

    visa_dict_sort = {}
    while len(visa_dict):
        minim = min(visa_dict)
        visa_dict_sort[minim] = visa_dict[minim]
        del visa_dict[minim]

    return visa_dict_sort


def write_data_visa_to_file():
    file_name = 'data_visa.pickle'
    data = get_info_visa()
    try:
        print(f'запись данных о визах в файл {file_name} началась.....')
        with open(file_name, 'wb') as f:
            pickle.dump(data, f)
        print(f'запись данных о визах в файл {file_name} успешно завершилась')
    except Exception as e:
        print(f'!!!! запись данных о визах в файл {file_name} не произошла. Ошибка {e}')


def get_data_visa_in_file():
    with open('data_visa.pickle', 'rb') as f:
        data = pickle.load(f)
    return data


# write_data_visa_to_file()
# res = get_info_visa()
# for i in res:
#     print(i, ' ', res[i])
