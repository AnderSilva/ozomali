
from .. import db, flask_bcrypt
import datetime
from app.main.model.blacklist import BlacklistToken
from ..config import key
import jwt
from typing import Union


class Produto(db.Model):    
    __tablename__ = "produto"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    nome = db.Column(db.String(100), unique=True, nullable=False)
    codigoBarra = db.Column(db.String(50), unique=True, nullable=True)
        
    
    def __repr__(self):
        return "<Produto '{}'>".format(self.nome)
