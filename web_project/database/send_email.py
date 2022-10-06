import smtplib, ssl
import os
from dotenv import load_dotenv
from message_log import *
import random
from message_formatter import *
from datetime import datetime, timedelta

load_dotenv()
EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER')
EMAIL_SENDER_ADDRESS = os.getenv('EMAIL_SENDER_ADDRESS')
EMAIL_SENDER_PASSWORD = os.getenv('EMAIL_SENDER_PASSWORD')
EMAIL_PORT = os.getenv('EMAIL_PORT')

#receiver_email = "carlos@gtel.ufc.br"
#confirmation_code = "753159"
#user_id = "897562"
#username = "carlosjun"

def send_confirmation_code(receiver_email, confirmation_code):
    try:
        message = f"""\
        Confirmation code

        Hello,

        This is your confirmation code: {confirmation_code}"""

        context = ssl.create_default_context()
        with smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_PORT) as server:
            server.starttls(context=context)
            server.login(EMAIL_SENDER_ADDRESS, EMAIL_SENDER_PASSWORD)
            server.sendmail(EMAIL_SENDER_ADDRESS, receiver_email, message)
    except Exception as e:
        print(e)

def create_confirmation_code(user_id, email):
    random_code = ''.join(map(str,random.sample(range(0,10), 5)))
    user_info = get_user_confirmation(user_id)
    if user_info:
        update_user_confirmation(user_id, random_code)
    else:
        create_confirmation_code_model(user_id, email, random_code)
    send_confirmation_code(email, random_code)

def check_confirmation_code(user_id, username, confirmation_code):
    user_info = get_user_confirmation(user_id)
    if user_info:
        user_info_datetime = user_info['created_at']
        if (datetime.now() - timedelta(minutes=5)) < user_info_datetime:
            if user_info['confirmation_code'] == confirmation_code:
                create_authorized_user(user_id, username)
                return True
        else:
            delete_user_confirmation(user_id)
    return False

def check_authorized_user(chat_id, username):
    user_info = get_authorized_user(chat_id)
    if user_info:
        if user_info['username'] == username:
            return True
    return False




    
