import requests
from bs4 import BeautifulSoup
from polimorph import ends_of_words
import pickle



HOST = 'https://f-gl.ru/'
URL = 'https://f-gl.ru/%D1%84%D0%BB%D0%B0%D0%B3%D0%B8-%D1%81%D1%82%D1%80%D0%B0%D0%BD-%D0%BC%D0%B8%D1%80%D0%B0/'
HEADERS = {
    "accept": 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
}

rules: list


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_link_all_flags():
    global rules
    rules2 = {}
    html = get_html(URL)
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('tbody')
    rules = []
    for it in items:
        for j in it('tr'):
            rules.append(
                {
                    'contry': ends_of_words(j.find('td').find('img').get('alt')),
                    'flag_link': HOST + j.find('td').find('img').get('src')
                }
            )
            rules2[ends_of_words(j.find('td').find('img').get('alt'))] = HOST + j.find('td').find('img').get('src')
    return rules2


def get_link_flag(req):
    global rules
    html = get_html(URL)
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('tbody')
    rules = []
    rules2 = {}

    for it in items:
        for j in it('tr'):
            if ends_of_words(j.find('td').find('img').get('alt')) == req:
                rules.append(
                    {
                        'contry': ends_of_words(j.find('td').find('img').get('alt')),
                        'flag_link': HOST + j.find('td').find('img').get('src')
                    }
                )
                rules2[ends_of_words(j.find('td').find('img').get('alt'))] = HOST + j.find('td').find('img').get('src')
    return rules2


def write_data_flag_to_file():
    data = get_link_all_flags()
    file_name = 'data_flags.pickle'
    try:
        print(f'    - запись данных флаги в файл {file_name} началась.....')
        with open(file_name, 'wb') as f:
            pickle.dump(data, f)
        print(f'    - запись данных флаги в файл {file_name} завершилась успешно')
    except Exception as e:
        print(f'    - !!!! запись данных флаги в файл {file_name} не произогла. Ошибка {e}')


def get_data_flag_in_file():
    with open('data_flags.pickle', 'rb') as f:
        data = pickle.load(f)
    return data


# write_data_flag_to_file()

# dat: dict
# dat = get_data_flag_in_file()
# for i in dat:
#     print(f'{i}: {dat[i]}')

# rules = get_link_all_flags()
#
# for i in rules:
#     print(i)
