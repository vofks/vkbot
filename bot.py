import vk
import connect
from  datetime import  datetime
import time

def handle(user_id, msg):
    db = connect.DB()
    msg = msg.lower();
    print(user_id,msg)
    if "get link" in msg:
        db.push_action(user_id,"get link")
    elif "get week":
        db.push_action(user_id,"get week")
    else:
        db.push_action(user_id,"help")



for i in range(18):
    time.sleep(3)
    last_messages = vk.get_last_messages()
    db = connect.DB()
    for msg_obj in last_messages:
        user_id = vk.get_id_by_msg(msg_obj)
        if msg_obj["out"]==1 and "admin_author_id" not in msg_obj:
            continue
        date = datetime.fromtimestamp(msg_obj['date']).strftime('%Y-%m-%d %H:%M:%S')
        if db.check_last_msg(user_id,date):
            print(msg_obj)
            handle(user_id,msg_obj["text"])