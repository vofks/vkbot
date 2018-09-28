import connect
import vk
import datetime
import time
from math import floor

def get_week():
    first_monday = datetime.date(2018,9,3)
    today = datetime.date.today()
    weeks_delta = (today - first_monday).days//7
    return weeks_delta%2==1


class Handler:
    def __init__(self):
        self.actions = {}

    def add_action(self,action, func):
        self.actions[action] = func

    def handle(self, user_id, action):
        db = connect.DB()
        if action in self.actions:
            self.actions[action](user_id)


def action_help(user_id):
    vk.send_hello(user_id)

def action_get_link(user_id):
    vk.send_to_one(user_id, db.get_link_and_date_str())

def action_get_week(user_id):
    week = "верхняя" if get_week() else "нижняя"
    vk.send_to_one(user_id, week)

handler = Handler()
handler.add_action("help",action_help)
handler.add_action("get week", action_get_week)
handler.add_action("get link", action_get_link)

while True:
    time.sleep(0.1)
    db = connect.DB()
    user_id,action = db.pop_action()
    if user_id and action:
        print(user_id,action)
    handler.handle(user_id,action)

