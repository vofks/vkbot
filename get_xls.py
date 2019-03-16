# -*- coding: utf-8 -*-

import requests, re

url = 'http://www.itmm.unn.ru/files/2019/03/1kurs-5.xls'

def download(url):
    try:
        fname = ''
        a = requests.get(url)
        print(a.status_code)
        res = re.search(r'\w+.?\w+\.\w+$', url)
        
        #with open(fname, 'wb') as f:
            #f.write(a.content)
    except requests.exceptions.RequestException as e:
        print(e)
        
    
if __name__ == "__main__":
    download(url)
