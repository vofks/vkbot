# -*- coding: utf-8 -*-

import requests, serializer
from bs4 import BeautifulSoup

url = 'http://www.itmm.unn.ru/studentam/raspisanie/raspisanie-bakalavriata-i-spetsialiteta-ochnoj-formy-obucheniya/'

def get_url():
    try:
        a = requests.get(url)
        a.encoding = 'utf-8'
        print (a.status_code)        
        return a.text
    except requests.ConnectionError:
        print('ConnectionError')
    except requests.HTTPError:
        print('HTTPError')
    except requests.Timeout:
        print('Connection timeout')
    except requests.TooManyRedirects:
        print('TooManyRedirects')
        
def parse_url():
    links = []
    page = get_url()
    soup = BeautifulSoup(page, 'lxml')
    for link in soup.find_all('a', string='скачать'):
        s = str(link.get('href'))
        print(s)
        links.append(s)
    if serializer.check(links):
        print('Send difference to user')
    
if __name__ == "__main__":
    parse_url()
