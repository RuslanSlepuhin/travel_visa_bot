
import requests
from bs4 import BeautifulSoup
import re
import pickle
import sys

HOST = 'https://traveling.by/'
URL = 'https://traveling.by/news/item/1590/'

HEADERS = {
    "accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
}

dict_country_free_visa = {}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r.text


def get_free_visa_info(country=None):

    html = get_html(URL)
    soup = BeautifulSoup(html, 'html.parser')

    container = soup.find(itemprop="articleBody")

    dictionary_country = {}
    title, description, country = [], [], []

    for i in container:
        if '<ul>' in str(i):
            country.append(i)
        if '<h2>' in str(i):
            title.append(i)
        if '<p>' in str(i):
            description.append(i)

    description.pop(8)
    for i in range(1, 6):
        description.pop(0)
    for i in range(1, 6):
        description.pop(-1)
    description.pop(1)
    description.pop(3)
    country.pop(1)

    d = {}
    free_countries = str(country[0]).split('</li>')
    d = separate_country(free_countries, 'без ограничений')
    dictionary_country[clean_text(str(title[0]))] = [d]

    d = {}
    free_countries = str(country[1]).split('</li>')
    d = separate_country(free_countries, 'без ограничений')
    dictionary_country[clean_text(str(title[1]))] = [d, clean_text(str(description[0])), clean_text(str(description[1]))]

    d = {}
    free_countries = str(country[2]).split('</li>')
    d = separate_country(free_countries, 'без ограничений')
    dictionary_country[clean_text(str(description[5]))] = [d, clean_text(str(description[2])), clean_text(str(description[3])), clean_text(str(description[4]))]

    return dictionary_country


def separate_country(free_countries, text):
    d = {}
    for i in free_countries:
        clean = clean_text(str(i)).split('-')
        key = clean[0].strip(' ')
        key = clean_text(key)
        clean.pop(0)
        if not clean:
            clean = [text]
        country_info = ' '.join(clean).strip(' ')
        if key:
            d[change_name(key)] = country_info  # меняем имя на такое же как в других списках
    return d


def change_name(key):
    if key == 'Китайская Народная Республика,Гонконг, Макао':
        key = 'Китай'
    elif key == 'Микронезия (Федеративные Штаты)':
        key = 'Микронезия'
    return key


def clean_text(text):
    text = text.replace('<ul>', '').\
        replace('</ul>', '').\
        replace('<li>', '').\
        replace('<h2>', '').\
        replace('</h2>', '').\
        replace('<strong>', '').\
        replace('</strong>', '').\
        replace('—', '-').\
        replace('\xa0', '').\
        replace('<li dir="ltr">', '').\
        replace('<p dir="ltr">', '').\
        replace('</p>', '').\
        replace('<p>', '')
    return text


def print_d(res):
    print(res, f'\n\n\n')
    with open('res.txt', 'w') as file:
        file.write(str(res))

    for i in res:
        print(clean_text(str(i)))
        for j in res[i][0]:
            if j:
                print(f'{j}: {res[i][0][j]}')


def write_data_free_visa_to_file():
    sys.setrecursionlimit(10000)
    data = get_free_visa_info()
    file_name = 'data_free_visa.pickle'
    try:
        print(f'запись данных о безвизе в файл {file_name} началась.....')
        with open(file_name, 'wb') as f:
            pickle.dump(data, f)
        print(f'запись данных о безвизе внесены успешно в {file_name}')
    except Exception as e:
        print(f'!!!! запись данных о безвизе не внесены в {file_name}, ошибка {e}')


def get_data_free_visa_in_file():
    with open('data_free_visa.pickle', 'rb') as f:
        data = pickle.load(f)
    return data

# write_data_free_visa_to_file()

# data = get_free_visa_info()
# for i in data:
#     for j in data[i]:
#         for k in j:
#             print(k)
