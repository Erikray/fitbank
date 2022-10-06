from .base_model import *
from .db import DBContextManager
from datetime import datetime

def create(message_log):
    try:
        with DBContextManager() as session:
            session.add(message_log)
            session.commit()
            session.refresh(message_log)
        return message_log
    except Exception as e:
        print(e)

def create_authorized_user(chat_id, username):
    try:
        authorized_user_model = AuthorizedUsersModel(
                    chat_id=chat_id,
                    username=username,
                )
        
        message_log = create(authorized_user_model)
        return message_log
    except Exception as e:
        print(e)

def query_authorized_user(chat_id):
    try:    
        with DBContextManager() as session:
            user_authorized_info = session.query(AuthorizedUsersModel).get(chat_id)
        return user_authorized_info
    except Exception as e:
        print(e)

def create_confirmation_code_model(user_id, email, confirmation_code):
    try:
        confirmation_code_model = ConfirmationCodesModel(
                    user_id=user_id,
                    email=email,
                    confirmation_code=confirmation_code
                )
        
        message_log = create(confirmation_code_model)
        return message_log
    except Exception as e:
        print(e)

def query_users_confirmation():
    try:    
        with DBContextManager() as session:
            users_confirmation_info = session.query(ConfirmationCodesModel).all()
        return users_confirmation_info
    except Exception as e:
        print(e)

def query_user_confirmation(user_id):
    try:    
        with DBContextManager() as session:
            user_confirmation_info = session.query(ConfirmationCodesModel).get(user_id)
        return user_confirmation_info
    except Exception as e:
        print(e)

def update_user_confirmation(user_id, confirmation_code):
    try:    
        with DBContextManager() as session:
            user_confirmation_info = session.query(ConfirmationCodesModel).get(user_id)
            if user_confirmation_info:
                user_confirmation_info.confirmation_code = confirmation_code
                user_confirmation_info.created_at = datetime.now()
                session.commit()
            else:
                return False
    except Exception as e:
        print(e)

def delete_user_confirmation(user_id):
    try:    
        with DBContextManager() as session:
            user_confirmation_info = session.query(ConfirmationCodesModel).get(user_id)
            if user_confirmation_info:
                session.delete(user_confirmation_info)
                session.commit()
            else:
                return False
    except Exception as e:
        print(e)

def delete_authoerized_user(chat_id):
    try:    
        with DBContextManager() as session:
            user_authorized_info = session.query(AuthorizedUsersModel).get(chat_id)
            if user_authorized_info:
                session.delete(user_authorized_info)
                session.commit()
            else:
                return False
    except Exception as e:
        print(e)

def query_users_account():
    try:    
        with DBContextManager() as session:
            users_account_info = session.query(ContasModel).all()
        return users_account_info
    except Exception as e:
        print(e)

def create_user_account(username, nome, email, cpf, telefone, tipo_conta):
    try:
        saldo = 0.0
        account_user_model = ContasModel(
                    username=username,
                    saldo=saldo,
                    nome=nome,
                    email=email,
                    cpf=cpf,
                    telefone=telefone,
                    tipo_conta=tipo_conta
                )   
        message_log = create(account_user_model)
        return message_log
    except Exception as e:
        print(e)

def delete_user_account(cpf):
    try:    
        with DBContextManager() as session:
            account_user_model = session.query(ContasModel).filter(ContasModel.cpf == cpf).first()
            if account_user_model:
                session.delete(account_user_model)
                session.commit()
            else:
                return False
    except Exception as e:
        print(e)