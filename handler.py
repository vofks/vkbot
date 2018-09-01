import connect
import vk

while True:
    db = connect.DB()
    user_id,action = db.pop_action()
    print(user_id,action)
    if action=="help":
        vk.send_hello(user_id)
    if action=="get link":
        date,link = db.get_current_link_and_date()
        vk.send_to_one(user_id,link+" от "+date)