from message_log import *

def all_users_confirmation():
    message_users_confirmation = query_users_confirmation()
    return [{"user_id":msg.user_id,"confirmation_code":msg.confirmation_code,
             "email":msg.email,"created_at":msg.created_at} 
             for msg in message_users_confirmation]

def all_users_account():
    message_users_account = query_users_account()
    return [{"user_id":msg.user_id,"username":msg.username,
             "saldo":msg.saldo} 
             for msg in message_users_account]

def get_user_confirmation(user_id):
    user = query_user_confirmation(user_id)
    if user:
        return {"user_id":user.user_id,"confirmation_code":user.confirmation_code,
                "email":user.email,"created_at":user.created_at}
    else:
        return False

def get_authorized_user(chat_id):
    user = query_authorized_user(chat_id)
    if user:
        return {"chat_id":user.chat_id,"username":user.username,
                "created_at":user.created_at}
    else:
        return False