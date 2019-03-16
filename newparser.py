# -*- coding: utf-8 -*-

import requests, serializer, get_xls
from bs4 import BeautifulSoup

url = 'http://www.itmm.unn.ru/studentam/raspisanie/raspisanie-bakalavriata-i-spetsialiteta-ochnoj-formy-obucheniya/'

def get_url():
    try:
        a = requests.get(url)
        a.encoding = 'utf-8'
        print(a.status_code)        
        return a.text
    except requests.exceptions.RequestException as e:        
        print('ConnectionError')
        return False
    
def parse_url():
    links = []
    page = get_url()
    if page:
        message = ''
        soup = BeautifulSoup(page, 'lxml')
        for link in soup.find_all('a', string='скачать'):
            s = str(link.get('href'))
            print(s)
            links.append(s)
        diff = serializer.check(links)
        if (diff):
            print('Send difference to user')
            for newLink in diff:
                message += '\n' + newLink
                get_xls.download(newLink)
            #vk.send_to_all(message)
    
if __name__ == "__main__":
    parse_url()
