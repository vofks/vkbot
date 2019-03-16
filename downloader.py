# -*- coding: utf-8 -*-

import requests

url = 'http://www.itmm.unn.ru/files/2019/03/1kurs-1.xls'

def download(url):
    with open('1.xls', 'w') as f:
        f.write(requests.get(url).text)
    
if __name__ == "__main__":
    download(url)
