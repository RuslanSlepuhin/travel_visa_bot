
import requests
from bs4 import BeautifulSoup
import re

HOST = 'https://www.tuda-suda.by/'
URL = 'https://www.tuda-suda.by/poleznyashki/turkhaki/3015-spisok-bezvizovykh-stran-dlya-belorusov-na-2022-god/'

HEADERS = {
    "accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def list_countries(mass):
    list_count = []
    for i in mass:
        res = i.split('\n')[0]
        list_count.append(res)
    print(list_count)

    return list_count


def get_info_bszvis(country=None):

    html = get_html(URL)
    soup = BeautifulSoup(html.text, 'html.parser')

    block = soup.find_all('tr', style='border-bottom: 1px solid #f9f9f9;')
    not_visa = []
    for i in block:
        not_visa.append(i.findAll('td'))

    mass = []
    line = ''
    for i in not_visa:
        if line:
            mass.append(line)
            line = ''
        for j in i:
            if '<td><a href=' in str(j):
                pass
            else:
                line = line + str(clean_text(j)) + f'\n'
    if not country:
        return mass
    else:
        print(mass)
        for i in mass:
            j = i.split(f'\n')[0]
            if country == j:
                return [i]





def clean_text(text):
    dirty_words = [
        '<td>',
        '</td>',
        '<strong>',
        '</strong>',
        '<a>',
        '</a>',
        '<br',
        '/br',

    ]
    text = str(text)
    if '<img alt=' in text:
        text = text.split()[-1]
    elif text == 'src="/images/countries_thumb/16.png"/>Мадагаскар':
        text = 'Мадагаскар'
    elif text == 'Россия':
        text = 'Российская Федерация'
    elif text == 'Сейшельские острава':
        text = 'Сейшельские острова'

    for i in dirty_words:
        text = text.replace(i, '')

    return text




res = (get_info_bszvis('Сингапур'))

print(res)
