
import requests
from bs4 import BeautifulSoup
import re

class Flags:


    def __init__(self, country):
        self.host = 'https://f-gl.ru/'
        self.url = 'https://f-gl.ru/%D1%84%D0%BB%D0%B0%D0%B3%D0%B8-%D1%81%D1%82%D1%80%D0%B0%D0%BD-%D0%BC%D0%B8%D1%80%D0%B0'
        self.headers = {
            "accept": 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
        }
        self.html = None
        self.flags = []
        self.country = country



    def get_content(self, country='Belarus'):
        self.html = get_html(self)
        soup = BeautifulSoup(self.html, 'html.parser')
        items = soup.find_all('div', itemprop='articleBody')
        self.flags = []

        for i in items:
            self.flags.append(
                {
                    'contry': i.find('table').find('tbody').find('tr').find('td').find('img').get('alt'),
                    'flag_link': i.find('table').find('tbody').find('tr').find('td').find('img').get('src')
                }
            )
        return self.flags


    def get_html(self):
        r = requests.get(self.url, headers=self.headers, params=params)
        return r

u = Flags('belarus')
print(u.get_content())



