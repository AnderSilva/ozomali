from .. import db, flask_bcrypt
import datetime
from ..config import key
from typing import Union

class Perfil(db.Model):
    __tablename__ = "perfil"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), index=False, unique=True, nullable=False)
    usuarios = db.relationship('Usuario', backref='perfil')
    ativo = db.Column(db.Boolean,default=True)    

    def __repr__(self):
        return "<Perfil {}>".format(self.nome)
