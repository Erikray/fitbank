from .message_log import *
import random
import string

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

def get_random_string(length):
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return result_str

def create_lead(chat_id, username, nome, email, cpf, telefone, tipo_conta):
    token = get_random_string(15)
    print(token)
    user = create_user_lead(chat_id, username, nome, email, cpf, telefone, tipo_conta, token)
    if user:
        return token
    else:
        return False

def get_lead(token):
    user = query_user_lead(token)
    if user:
         return {"id":user.id, "username": user.username,
                 "chat_id":user.chat_id, "email": user.email,
                 "nome":user.nome, "cpf": user.cpf, "telefone":user.telefone,
                 "tipo_conta": user.tipo_conta, "created_at":user.created_at}
    else:
        return False

def get_user_cpf(cpf):
    user = query_user_account_cpf(cpf)
    if user:
         return {"user_id":user.user_id, "username": user.username,
                 "saldo":user.saldo, "email": user.email,
                 "nome":user.nome, "cpf": user.cpf, "telefone":user.telefone,
                 "tipo_conta": user.tipo_conta}
    else:
        return False

def get_user_username(username):
    user = query_user_account_username(username)
    if user:
         return {"user_id":user.user_id, "username": user.username,
                 "saldo":user.saldo, "email": user.email,
                 "nome":user.nome, "cpf": user.cpf, "telefone":user.telefone,
                 "tipo_conta": user.tipo_conta}
    else:
        return False