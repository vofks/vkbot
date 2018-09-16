import vk
import connect
import datetime
import time
import json

def handle(user_id, msg):
    db = connect.DB()
    msg = msg.lower();
    print(user_id,msg)
    if "get link" in msg:
        db.push_action(user_id,"get link")
    elif "get week" in msg:
        db.push_action(user_id,"get week")
    else:
        db.push_action(user_id,"help")


server = vk.get_long_poll_server()
while True:
    time.sleep(1)
    try:
        events = vk.get_new_messages(server)
    except (json.JSONDecodeError, KeyError):
        server = vk.get_long_poll_server()
        continue

    last_messages = events['updates']
    for msg_obj in last_messages:
        user_id = msg_obj['object']['user_id']
        handle(user_id, msg_obj['object']['body'])
