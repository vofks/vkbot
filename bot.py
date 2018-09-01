import vk
import connect
from  datetime import  datetime


def handle(user_id, msg):
    db = connect.DB()
    if "get link" in msg:
        db.push_action(user_id,"get link")
    else:
        db.push_action(user_id,"help")


while True:
    last_messages = vk.get_last_messages()
    db = connect.DB()
    for msg_obj in last_messages:
        user_id = vk.get_id_by_msg(msg_obj)
        if msg_obj["out"]==1 and "admin_author_id" not in msg_obj:
            continue
        date = datetime.fromtimestamp(msg_obj['date']).strftime('%Y-%m-%d %H:%M:%S')
        if db.check_last_msg(user_id,date):
            handle(user_id,msg_obj["text"])