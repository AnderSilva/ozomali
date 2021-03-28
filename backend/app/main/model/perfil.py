
from .. import db, flask_bcrypt
import datetime
from app.main.model.blacklist import BlacklistToken
from ..config import key
import jwt
from typing import Union


class Perfil(db.Model):    
    __tablename__ = "perfil"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), index=False, unique=True, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

    def __repr__(self):
        return "<Perfil {}>".format(self.nome)
