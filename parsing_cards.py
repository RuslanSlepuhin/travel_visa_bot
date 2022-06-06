
import requests
from bs4 import BeautifulSoup


HOST = 'https://minfin.com.ua/'
URL = 'https://minfin.com.ua/cards/'
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='sc-182gfyr-0')
    cards = []

    print('type items: ', type(items))
    print('items = ', items)

    for i in items:
        cards.append(
            {
                'title': i.find('div', class_='be80pr-9').find('a').get('alt'),
                'link_product': HOST + i.find('div', class_='be80pr-9').find('a').get('href'),
                'card_img': i.find('div', class_='be80pr-9').find('a').find('img').get('src'),
                'brand': i.find('div', class_='be80pr-16').find('a').get('alt')

            }
        )
    return cards


def parser():
    PAGENATION = input('укажите количество страниц для парсинга: ')
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        for page in range(1, PAGENATION):
            print(f'Парсим страницу: {page}')
            html = get_html(URL, params={'page': page})
            cards.extend(get_content(html.text))
    else:
        print('Error')

    return cards


html = get_html(URL)
cards = get_content(html.text)
for i in cards:
    print(i, f'\n')
