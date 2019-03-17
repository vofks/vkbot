# -*- coding: utf-8 -*-

import requests, re, os

test = ['http://www.itmm.unn.ru/files/2019/03/1kurs.xls']

def download(urlList):
    dname = '\\data\\'
    path = os.getcwd() + dname   
    try:        
        for url in urlList:
            a = requests.get(url)
            print('HTTP status:', a.status_code)
            res = re.search(r'[^/]+\.\w+$', url)
            fname = url[res.start():res.end()]
            print(fname)
            tmpath = path + fname            
            with open(tmpath, 'wb') as f:
                f.write(a.content)
    except requests.exceptions.RequestException as e:
        print(e)        

if __name__ == "__main__":
    download(test)
