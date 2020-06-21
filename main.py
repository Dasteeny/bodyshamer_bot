import json
import datetime
import requests
from time import sleep

with open("config.json") as config:
    config_json = json.loads(config.read())
token = config_json['HTTP_API']


class BotHandler:
    def __init__(self, token):
        self.token = token
        self.api_url = f"https://api.telegram.org/bot{token}/"

    def get_updates(self, offset=None, timeout=30):
        method = "getUpdates"
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json


    def get_last_update(self):
        updates = self.get_updates()
        if len(updates) > 0:
            last_update = updates[-1]
        else:
            last_update = updates[len(updates)]
        return last_update


    def send_msg(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = "sendMessage"
        response = requests.post(self.api_url + method, params)
        return response


bodyshamer = BotHandler(token)
greetings = ("hello!", "good morning!", "good day!", "good evening!")
now = datetime.datetime.now()

def main():
    print(f"{now:%Y-%m-%d %H:%M:%S}::Bot started...")
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        bodyshamer.get_updates(new_offset)

        last_update = bodyshamer.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
            bodyshamer.send_msg(last_chat_id, f"Good morning, {last_chat_name}")
            today += 1
        elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
            bodyshamer.send_msg(last_chat_id, f"Good day, {last_chat_name}")
            today += 1
        elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
            bodyshamer.send_msg(last_chat_id, f"Good evening, {last_chat_name}")
            today += 1
    
    new_offset = last_update_id + 1


if __name__ == "__main__":
    try:
        print("Starting bot...")
        main()
    except KeyboardInterrupt:
        exit()
        print("Bot stopped.")
