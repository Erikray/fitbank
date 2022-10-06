import telebot
from telebot import types
import csv
import pandas as pd
import requests
import json
import os
from dotenv import load_dotenv
import logging

# for debug use logging.DEBUG
# for normal use logging.INFO
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
RASA_REST_API = os.getenv('RASA_REST_API')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def verify(message):
    return True


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    print(call.data)

@bot.message_handler(func=lambda message: True)
def new_contact(message):

    user_message = message.json['text']
    user_id = message.chat.id
    user_name = message.from_user.username

    logging.info(f'user_id: {user_id:} | user_name: {user_name} | user_message: {user_message}')
    logging.debug(message)

    sender_tag = user_name + ':' + str(user_id)

    json_message = {"sender":sender_tag, "message":user_message}
    print(json_message)
    response = requests.post(RASA_REST_API,json=json_message)
    response_json = json.loads(response.content)
    logging.debug(response_json)
    
    print(response_json)
    for bot_msg in response_json:
        response_text = bot_msg['text']
        #response_chat_id = bot_msg['recipient_id']
        if 'buttons' in bot_msg.keys():
            #markup = types.InlineKeyboardMarkup(row_width=2)
            markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
            for button in bot_msg['buttons']:
                if 'text' in button.keys():
                    #markup.add(types.InlineKeyboardButton(button['text'], callback_data='ok'))
                    markup.add(types.InlineKeyboardButton(button['text']))
            bot.send_message(user_id, response_text, reply_markup=markup)  
        else:  
            bot.send_message(user_id, response_text)
        logging.info(f'user_id: {user_id:} | bot_response_text: {response_text}')
    
bot.polling()


