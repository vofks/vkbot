import urllib.request
import connect
import vk
import re


def parse(html):
    a = html.find('бакалавров')
    if a != -1:
        date_begin = html.find('(', a)
        date_end = html.find(')', date_begin) + 1
        href = html.find('href', a)
        link_begin = html.find('"', href) + 1
        link_end = html.find('"', link_begin)

        link = html[link_begin:link_end]
        date = html[date_begin:date_end]
        reg = re.compile('[а-яА-Я]')
        date = reg.sub('', date)
        return date, link
    else:
        raise Exception("Не получается найти ссылку на странице")


def get_html():
    url = 'http://www.itmm.unn.ru/studentam/raspisanie/'
    resp = urllib.request.urlopen(url)
    if resp.code == 200:
        html = resp.fp.read(resp.length).decode("utf-8")
        return html
    else:
        raise Exception("Страница не доступна")


html = get_html()
date, link = parse(html)
db = connect.DB()
if db.update_link(date, link):
    vk.send_to_all(link + " от " + date)



