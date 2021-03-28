
from .. import db, flask_bcrypt
import datetime
from app.main.model.blacklist import BlacklistToken
from ..config import key
import jwt
from typing import Union


class Vendor(db.Model):    
    __tablename__ = "fornecedor"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    cnpj = db.Column(db.String(128), unique=True, nullable=False)
    nome = db.Column(db.String(128), unique=True, nullable=False)
    logradouro = db.Column(db.String(128), nullable=False)
    complemento = db.Column(db.String(128), nullable=False)
    bairro = db.Column(db.String(128), nullable=False)
    cidade = db.Column(db.String(128), nullable=False)
    estado = db.Column(db.String(128), nullable=False)
    cep = db.Column(db.String(128), nullable=False)        
    ativo = db.Column(db.Boolean,default=True)       

    def __repr__(self):
        return "<Usuario '{}'>".format(self.login)
