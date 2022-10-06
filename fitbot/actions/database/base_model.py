from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

BaseModel = declarative_base()

class ConfirmationCodesModel(BaseModel):
    __tablename__ = "confirmation_codes"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False)
    confirmation_code = Column(String(255), nullable=False)
    created_at = Column(
        DateTime, server_default=func.current_timestamp(), nullable=False
    )

class ContasModel(BaseModel):
    __tablename__ = "contas"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    saldo = Column(Float(4), nullable=False)
    email = Column(String(255), nullable=True)
    nome = Column(String(255), nullable=True)
    cpf = Column(String(255), nullable=True)
    telefone = Column(String(255), nullable=True)
    tipo_conta = Column(String(255), nullable=True)

class AuthorizedUsersModel(BaseModel):
    __tablename__ = "authorized_users"

    chat_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    created_at = Column(
        DateTime, server_default=func.current_timestamp(), nullable=False
    )

class LeadsModel(BaseModel):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=True)
    chat_id = Column(String(255), nullable=True)
    nome = Column(String(255), nullable=True)
    cpf = Column(String(255), nullable=True)
    telefone = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    tipo_conta = Column(String(255), nullable=True)
    token = Column(String(255), nullable=True)
    created_at = Column(
        DateTime, server_default=func.current_timestamp(), nullable=False
    )
