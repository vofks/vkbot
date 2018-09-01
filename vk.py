import urllib.parse
import urllib.request
import top_secret
from math import ceil
import json


admin_id = 59544463
send_url = "https://api.vk.com/method/messages.send"
token = top_secret.token
version = "5.0"
hello_msg = "Ты будешь получать прямые ссылки на расписание, когда оно будет меняться(но это не точно)"


def send_to_one(user_id, message):
    param = {
        'user_id': user_id,
        'message': message,
        'access_token': token,
        'v': version
    }
    url = send_url + '?' + urllib.parse.urlencode(param)
    resp = urllib.request.urlopen(url)


def send_hello(user_id):
    send_to_one(user_id, hello_msg)


def send_to_admin(message):
    send_to_one(admin_id, message)


def send_to_admin2(message):
    send_to_one(108186884, message)


def send_to_many(user_ids, message):
    param = {
        'user_ids': user_ids,
        'message': message,
        'access_token': token,
        'v': version
    }
    url = send_url + '?' + urllib.parse.urlencode(param)
    resp = urllib.request.urlopen(url)


def send_to_all(message):
    parts = get_users_by_parts(99)
    for hundredPart in parts:
        send_to_many(hundredPart, message)


def join_part(part):
    return ",".join(part)


def get_users_by_parts(N):
    result = []
    users = get_users()
    count_of_parts = ceil(len(users) / N)
    for i in range(count_of_parts):
        part = users[i * N:(i + 1) * N]
        result.append(join_part(part))
    return result


def get_users():
    url = 'https://api.vk.com/method/messages.getDialogs?'
    param = {
        'access_token': token,
        'v': version,
        'count': 200
    }
    url += urllib.parse.urlencode(param)
    resp = urllib.request.urlopen(url)
    js = json.loads(resp.fp.read(resp.length).decode("utf-8"))
    dialogs = js['response']['items']
    list_of_users = []
    for i in dialogs:
        check_url = 'https://api.vk.com/method/messages.isMessagesFromGroupAllowed?'
        check_param = {
            'group_id': 152709221,
            'user_id': i['user_id'],
            'access_token': token,
            'v': version
        }
        check_url += urllib.parse.urlencode(check_param)
        check_resp = urllib.request.urlopen(check_url)
        check_js = json.loads(check_resp.fp.read(check_resp.length).decode("utf-8"))
        is_allowed = check_js['response']['is_allowed']
        if is_allowed == 1:
            list_of_users.append(str(i['user_id']))
            print("+")
        else:
            print("-")

    return list_of_users


if __name__ == "__main__":
    get_users()