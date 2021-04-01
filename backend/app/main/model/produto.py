
from .. import db
import datetime
from ..config import key
from typing import Union
from .. model.fornecedor import Fornecedor

class Produto(db.Model):    
    __tablename__ = "produto"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    nome = db.Column(db.String(100), unique=True, nullable=False)
    codigoBarra = db.Column(db.String(50), unique=True, nullable=True)
    fornecedor_id = db.Column(db.Integer,db.ForeignKey('fornecedor.id'))

    ativo = db.Column(db.Boolean,default=True)
        
    
    def __repr__(self):
        return "<Produto '{}'>".format(self.nome)
