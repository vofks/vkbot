import connect
import vk
import datetime
import time
from math import floor

def get_week():
    first_monday = datetime.date(2018,9,3)
    today = datetime.date.today()
    weeks_delta = (today - first_monday).days//7
    return "верхняя" if weeks_delta%2==1 else "нижняя"


for i in range(18):
    time.sleep(3)
    db = connect.DB()
    user_id,action = db.pop_action()
    if user_id and action:
        print(user_id,action)
    if action=="help":
        vk.send_hello(user_id)
    if action=="get link":
        vk.send_to_one(user_id,db.get_link_and_date_str())
    if action=="get week":
        vk.send_to_one(user_id,get_week())

