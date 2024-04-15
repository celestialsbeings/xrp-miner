import requests
import json
import time
import os
from telegram import Bot
from keep_alive import keep_alive
keep_alive()

total_money = 0
Good = 0
Bad = 0

bot_token = '6897034474:AAHnFLDpsSXJSG03oIuAs0yKF2IWf8I0tbw'
chat_id = '5308059847'
bot = Bot(token=bot_token)


def Login():
    email = "celestialfromtg"
    password = "az11002021"

    headers = {
        'authority': 'faucetearner.org',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
        'content-type': 'application/json',
        'origin': 'https://faucetearner.org',
        'referer': 'https://faucetearner.org/login.php',
        'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'act': 'login',
    }

    json_data = {
        'email': email,
        'password': password,
    }

    response = requests.post('https://faucetearner.org/api.php', params=params, headers=headers, json=json_data)
    
    if "Login successful" in response.text:
        sufi = response.cookies.get_dict()
        print(f'Good Login')
        print(sufi)
        print(f'_' *60)   
        Money(sufi)
    elif "wrong username or password" in response.text:
        print(f'Bad Login')
    else:
        print(f'Error')

def Money(cookies):
    global total_money , Bad , Good
    while True:
        time.sleep(5)
        headers = {
            'authority': 'faucetearner.org',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
            'origin': 'https://faucetearner.org',
            'referer': 'https://faucetearner.org/faucet.php',
            'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        params = {
            'act': 'faucet',
        }

        json_data = {}

        rr = requests.post('https://faucetearner.org/api.php', params=params, cookies=cookies, headers=headers).text
        
        if 'Congratulations on receiving' in rr:
            Good += 1
            json_data = json.loads(rr)
            message = json_data["message"]
            start_index = message.find(">") + 1
            end_index = message.find(" ", start_index)
            balance = message[start_index:end_index]
            total_money += float(balance)
            balance = f"[{Good}]Done {balance} XRP£. Total money: {total_money}"
            bot.send_message(chat_id=chat_id, text=f"Your balance is: {balance} XRP£")
        elif 'You have already claimed, please wait for the next wave!' in rr:
            Bad += 1
        else:
            print(f'Erorr')


Login()
