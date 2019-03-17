# -*- coding: utf-8 -*-

import requests, serializer, loader
from bs4 import BeautifulSoup

url = 'http://www.itmm.unn.ru/studentam/raspisanie/raspisanie-bakalavriata-i-spetsialiteta-ochnoj-formy-obucheniya/'
debug = False

def get_url():
    try:
        a = requests.get(url)
        a.encoding = 'utf-8'
        print('HTTP status:', a.status_code)        
        return a.text
    except requests.exceptions.RequestException as e:        
        print('ConnectionError')
        return 0
    
def parse_url():
    links = []
    page = get_url()
    if page:
        message = ''
        soup = BeautifulSoup(page, 'lxml')
        print('Links:')
        for link in soup.find_all('a', string = 'скачать'):
            s = str(link.get('href'))
            print(s)
            links.append(s)
        diff = serializer.check(links)
        if (diff):
            print('Send difference to user')
            for newLink in diff:
                message += newLink + '\n'
            print(message)
            if not debug:
                loader.download(diff)
                #vk.send_to_all(message)
    
if __name__ == "__main__":
    parse_url()
