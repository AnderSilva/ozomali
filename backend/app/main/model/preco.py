
from .. import db
import datetime
from ..config import key
from typing import Union
from sqlalchemy import func
from .. model.movimentacao import Movimentacao
from .. model.usuario import Usuario
from .. model.produto import Produto
from .. model.contato import Contato

class Preco(db.Model):    
    __tablename__ = "preco"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)        
    precoVenda = db.Column(db.Float, nullable=False)
    dataEmissao = db.Column(db.DateTime(timezone=True),server_default=func.now())
    status = db.Column(db.String(10), nullable=False)
    ativo = db.Column(db.Boolean,default=True)
    usuario_id = db.Column(db.Integer,db.ForeignKey('usuario.id'))
    produto_id = db.Column(db.Integer,db.ForeignKey('produto.id'))
