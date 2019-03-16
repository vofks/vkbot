# -*- coding: utf-8 -*-

import requests, re

url = 'http://www.itmm.unn.ru/files/2019/03/1kurs.xls'

def download(url):
    try:
        a = requests.get(url)
        print(a.status_code)
        res = re.search(r'[^/]+\.\w+$', url)
        fname = url[res.start():res.end()]
        print(fname)
        with open(fname, 'wb') as f:
            f.write(a.content)
    except requests.exceptions.RequestException as e:
        print(e)        
    
if __name__ == "__main__":
    download(url)
