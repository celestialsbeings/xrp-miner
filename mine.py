import requests
import json
import time
import os
import threading
from telegram import Bot
from telegram.ext import Updater, CommandHandler
from keep_alive import keep_alive
keep_alive()

total_money = 0
Good = 0
Bad = 0
balance = 0

bot_token = '6897034474:AAG0U74_pdWABW8UMlOtpkyuEOm4SI2LvJQ'
chatid = '5308059847'
# bot = Bot(token=os.environ.get('token'))

def Login(email, password):
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

    response = requests.post('https://faucetearner.org/api.php', params=params, headers=headers, json=json_data, timeout=10)

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
    global total_money, Bad, Good, balance

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

    rr = requests.post('https://faucetearner.org/api.php', params=params, cookies=cookies, headers=headers, timeout=10).text

    if 'Congratulations on receiving' in rr:
        Good += 1
        json_data = json.loads(rr)
        message = json_data["message"]
        start_index = message.find(">") + 1
        end_index = message.find(" ", start_index)
        balance = message[start_index:end_index]
        total_money += float(balance)
        message = f"[{Good}]Done {balance} XRP£. Total money: {total_money}"
    elif 'You have already claimed, please wait for the next wave!' in rr:
        Bad += 1
    else:
        print(f'Error')

def infiloop():
    while True:
        time.sleep(5)
        Login("celestialfromtg", "az11002021")

def check(update, context):
    global total_money, Good, Bad, balance
    message = f"Total money: {total_money}\nTotal account have: {Good}\nTotal Balance :{balance}"
    context.bot.send_message(chat_id=chatid, text=message)

def main():
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    check_handler = CommandHandler('check', check)
    dispatcher.add_handler(check_handler)

    updater.start_polling()

    # Start the loop in a separate thread
    loop_thread = threading.Thread(target=infiloop)
    loop_thread.start()

    updater.idle()

if __name__ == "__main__":
    main()
