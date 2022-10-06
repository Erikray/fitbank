from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import json
from telegram import send_message
from database.message_log import (
    create_user_account, 
    create_authorized_user, 
    delete_user_account,
    delete_authoerized_user,
)
from database.message_formatter import get_lead

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="static/templates")

@app.get("/cadastro/{token}", response_class=HTMLResponse)
async def read_cadastro(request: Request, token: str):
    user_info = get_lead(token)
    name = user_info['nome']
    return templates.TemplateResponse("cadastro.html", {"request": request, "name": name, "token": token})

@app.post("/confirmar", response_class=HTMLResponse)
async def read_cadastro(request: Request):
    request_form = await request.form()
    token = request_form.get('token')
    user_info = get_lead(token)

    chat_id = user_info['chat_id']
    username = user_info['username']
    nome = user_info['nome']
    cpf = user_info['cpf']
    telefone = user_info['telefone']
    email = user_info['email']
    tipo_conta = user_info['tipo_conta']

    # todo: confirm the creation of account
    delete_authoerized_user(chat_id)
    create_authorized_user(chat_id, username)
    delete_user_account(cpf)
    create_user_account(username, nome, email, cpf, telefone, tipo_conta)
    
    message=f"Parabéns {nome}, sua conta foi criada com sucesso!"
    send_message(chat_id, message)
    message="Você já pode baixar o aplicativo do banco e acessar sua conta usando CPF e senha"
    send_message(chat_id, message)
    message="Por aqui, vou conseguir te ajudar nas seguintes operações:\n\n- Consultar saldo\n- Fazer um pix\n- Pagar uma conta\n"
    send_message(chat_id, message)

    return templates.TemplateResponse("confirmar.html", {"request": request, "nome": nome})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)