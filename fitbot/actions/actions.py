# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from .database.message_formatter import (
    create_lead,
    get_user_cpf,
    get_user_username
)
from .database.send_email import (
    create_confirmation_code,
    check_confirmation_code,
    check_authorized_user
)

class ActionRequestForPhoto(Action):

    def name(self) -> Text:
        return "action_request_for_photo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_name = tracker.get_slot("user_name")
        account_type = tracker.get_slot("account_type")
        user_cpf_number = tracker.get_slot("user_cpf_number")
        user_email = tracker.get_slot("user_email")
        user_phone_number = tracker.get_slot("user_phone_number")
        print(f"user_name: {user_name}")
        print(f"account_type: {account_type}")
        print(f"user_cpf_number: {user_cpf_number}")
        print(f"user_email: {user_email}")
        print(f"user_phone_number: {user_phone_number}")
        sender_id = tracker.current_state()['sender_id']
        username, chat_id  = sender_id.split(':')
        token = create_lead(chat_id, username, user_name, user_email, user_cpf_number, user_phone_number, account_type)
        dispatcher.utter_message(text="Para concluir o seu cadastro você deve acessar o link:")
        dispatcher.utter_message(text=f"https://chat.gtel.ufc.br/cadastro/{token}")
        return []

class ActionLoginWithCPF(Action):

    def name(self) -> Text:
        return "action_login_with_cpf"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        sender_id = tracker.current_state()['sender_id']
        username, chat_id  = sender_id.split(':')
        user_cpf_number = tracker.get_slot("user_cpf_number")
        user = get_user_cpf(user_cpf_number)
        if user:
            email = user['email']
            create_confirmation_code(chat_id, email)
            dispatcher.utter_template('utter_inform_login_code', tracker)
            #dispatcher.utter_message(text="Um código de verificação foi enviado para o seu email")
            print(user['cpf'])
            print(user_cpf_number)
            return [SlotSet("valid_cpf", user_cpf_number),
                    SlotSet("user_cpf_number", user_cpf_number)]
        else:
            dispatcher.utter_message(text="CPF não encontrado.")
            dispatcher.utter_message(text="Pode tentar novamente?")
            return [SlotSet("valid_cpf", None)]

class ActionCheckLoginCode(Action):

    def name(self) -> Text:
        return "action_check_login_code"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        sender_id = tracker.current_state()['sender_id']
        username, chat_id  = sender_id.split(':')
        login_code = tracker.get_slot("login_code")
        check_user = check_confirmation_code(chat_id, username, login_code)
        if check_user:
            dispatcher.utter_message(text="Código confirmado!")
            dispatcher.utter_template("utter_inform_available_options", tracker)
        else:
            dispatcher.utter_message(text="Código não confirmado")
            dispatcher.utter_template("utter_inform_login_code", tracker)
        return []

class ActionResetSlots(Action):

    def name(self) -> Text:
        return 'action_reset_slots'

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet('account_type', None), SlotSet('user_name', None),
                SlotSet('user_cpf_number', None), SlotSet('user_email', None), 
                SlotSet('user_phone_number', None), SlotSet('login_code', None)]

class ActionQueryBalance(Action):

    def name(self) -> Text:
        return "action_query_balance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        sender_id = tracker.current_state()['sender_id']
        username, chat_id  = sender_id.split(':')
        check_user = check_authorized_user(chat_id, username)
        if check_user:
            #user_cpf_number = tracker.get_slot("user_cpf_number")
            #print(user_cpf_number)
            #user = get_user_cpf(user_cpf_number)
            user = get_user_username(username)
            print(user)
            if user:
                dispatcher.utter_message(text=f"Saldo da sua conta é de R$ {user['saldo']}")
            else:
                dispatcher.utter_message(text="Usuário não encontrado.")
        else:
            dispatcher.utter_message(text="Usuário não autorizado")
        return []

class ActionTransferMoney(Action):

    def name(self) -> Text:
        return "action_transfer_money"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        sender_id = tracker.current_state()['sender_id']
        username, chat_id  = sender_id.split(':')
        check_user = check_authorized_user(chat_id, username)
        if check_user:
            user_cpf_number = tracker.get_slot("user_cpf_number")
            user = get_user_cpf(user_cpf_number)
            if user:
                #transfer_value = tracker.get_slot("quant_transfer")
                #acc_target = tracker.get_slot("account_id")
                dispatcher.utter_message(text=f"Saldo da sua conta é de R$ {user['saldo']}")
            else:
                dispatcher.utter_message(text="Usuário não autorizado")
        return []

        
