
from .. import db
import datetime
from ..config import key
from typing import Union
from sqlalchemy import func
from .. model.tipocontato import TipoContato
from .. model.fornecedor import Fornecedor


class Contato(db.Model):
    __tablename__ = "contato"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    valor  = db.Column(db.String(100), nullable=False)

    ativo = db.Column(db.Boolean,default=True)
    tipocontato_id = db.Column(db.Integer,db.ForeignKey('tipocontato.id'))
    fornecedor_id = db.Column(db.Integer,db.ForeignKey('fornecedor.id'))