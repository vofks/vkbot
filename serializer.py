# -*- coding: utf-8 -*-

import json, os

fname = 'links.json'
dname = '\\data\\'
fpath = os.getcwd() + dname + fname

def write(newLinks):
    print('serialize')
    with open(fpath, 'w') as f:
        json.dump(newLinks, f)
        f.close

def read():
    print('deserialize')
    try:
        with open(fpath, 'r') as f:
            data = json.load(f)
            f.close()
            return data      
    except (OSError, IOError):
        print('I/O Error')
        with open(fpath, 'w') as f:
            f.close()
            read()            
                    
def check(newLinks):
    print('check')
    try:
        oldLinks = read()
    except json.JSONDecodeError as err:
        print('ERROR (is json empty?) ' + str(err))
        write(newLinks)
        return newLinks
    diff = list(set(newLinks) - set(oldLinks))
    if not diff:
        print('no difference')
        return 0
    else:
        print('Difference: ' + str(diff))
        write(newLinks)
        return diff
    
    
