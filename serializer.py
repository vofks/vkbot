# -*- coding: utf-8 -*-

import json

def write(newLinks):
    print('serialize')
    with open('links.json', 'w') as wf:
        json.dump(newLinks, wf)
        wf.close

def read():
    print('deserialize')
    with open('links.json', 'r') as rf:
        data = json.load(rf)
        rf.close()
        return data      
            

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
    
