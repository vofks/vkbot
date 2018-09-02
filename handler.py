import connect
import vk

for i in range(100):
    db = connect.DB()
    user_id,action = db.pop_action()
    if user_id and action:
        print(user_id,action)
    if action=="help":
        vk.send_hello(user_id)
    if action=="get link":
        vk.send_to_one(user_id,db.get_link_and_date_str())