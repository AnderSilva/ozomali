from .. import db
import datetime
from ..config import key
# import jwt
from typing import Union


class Fornecedor(db.Model):    
    __tablename__ = "fornecedor"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    logradouro = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    complemento = db.Column(db.String(20), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    cep = db.Column(db.String(8), nullable=False)        
    ativo = db.Column(db.Boolean,default=True)       

    def __repr__(self):
        return "<Nome '{}'>".format(self.nome)
