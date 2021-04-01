
from .. import db
import datetime
from ..config import key
from typing import Union
from sqlalchemy import func


class TipoContato(db.Model):    
    __tablename__ = "tipocontato"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)        
    nome  = db.Column(db.String(50), nullable=False)    
    
    ativo = db.Column(db.Boolean,default=True)
    # perfil_id = db.Column(db.Integer,db.ForeignKey('perfil.id'))       
