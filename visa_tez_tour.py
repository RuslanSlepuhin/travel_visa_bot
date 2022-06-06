import requests
from bs4 import BeautifulSoup
import re
import pickle


HOST = 'https://www.tez-tour.com/'
URL = 'https://www.tez-tour.com/covid19.html'

URL_DICT = {

}

HEADERS = {
    "accept":
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/'
        'apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    "user-agent":
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36'
}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r.text


def get_covid_info_tez():

    covid = {}
    covid_info_temp = ''
    update = ''

    html = get_html(URL)
    soup = BeautifulSoup(html, 'html.parser')
    container = soup.find_all('div', class_='news-item')
    # print(f'Connect with {URL} Response 200')

    with open('tex.txt', 'w') as f:
        f.write('covid-19 info')

    for i in container:
        country = i.find('div', class_='news-title').text
        # print('country = ', country)
        if country == "КИТАЙ (КНР)":
            country = 'Китай'
        elif country == 'Танзания (о. Занзибар)':
            country = 'Танзания'
        last_date = i.find('div', class_='news-date').text.strip()
        last_date = re.sub(r'\s{2,}', '', last_date)
        # print('last_date = ', country, last_date)

        covid_info = i.find_all('div', 'news-desc')
        # print('covid_info = ', country, covid_info)

        line = ''
        for j in covid_info:
            line = line + str(j)
        if country != "ОАЭ":
            country = country.capitalize()
        if country != 'Остальные страны':
            covid[country] = f'\n{last_date} {clear_text_re(line)}'
        else:
            update = i.find('div', class_='news-date').text
            update = re.sub(r"'*\s{2,}'*", '', update)
            covid_info_temp = line

    covid_info_temp = covid_info_temp.split('<tr>')
    covid_info_temp.pop(0)
    for i in covid_info_temp:
        spl = i.split('</th>')
        country = spl[0].replace('\n', '')
        line = spl[1]
        line = re.sub(r"\n{2,}", f'\n', f'{update}\n\n' + clear_text_re(line))
        covid[clear_text_re(country)] = line

    covid_sort = {}
    while len(covid):
        minim = min(covid)
        if minim == 'Танзания (о. Занзибар)':
            covid_sort['Танзания'] = covid[minim]
        else:
            covid_sort[minim] = covid[minim]
        del covid[minim]

    return covid_sort


def write_covid_tez_to_file():
    covid_sort = get_covid_info_tez()
    file_name = 'data_covid_tez.pickle'
    try:
        print(f'    - запись данных о covid-19 в файл {file_name} началась.....')
        with open(file_name, 'wb') as f:
            pickle.dump(covid_sort, f)
            print(f'    - запись данных о covid-19 в файл {file_name} завершилась успешно')
    except Exception as e:
        print(f'    - !!!!Ошибка {e} записи данных о covid-19 в файл {file_name}')


def read_covid_tez_in_file():
    with open('data_covid_tez.pickle', 'rb') as f:
        covid_sort = pickle.load(f)
    return covid_sort


def clear_text_re(text):
    text = re.sub(r'<.{1,7}/>', '', text)
    text = re.sub(r'</.>', '', text)
    text = re.sub(r'"*\s*[\n]*<*[a-z]\s*\w+="[_blank">]*', ' ', text)
    text = text.replace('<p>', f'\n').\
        replace('<li>', f'\n    - ').\
        replace('<ul>', '')
    text = re.sub(r'</*\w+\s*\w+-*\w*:*\s*\w*;*"*>', '', text)
    text = re.sub(r'<tabl.*', '', text)
    text = re.sub(r'<h.+>', '', text)
    text = re.sub(r'\n{2,}', '\n', text)
    text = text.replace('">', ', ')
    text = re.sub(r'<im\s+', '', text)

    return text


# write_covid_tez_to_file()
# res = get_covid_info_tez()
#
# with open('tez.txt', 'a') as f:
#     for i in res:
#         print(f'{str(i)}: {str(res[i])}')
# pass
