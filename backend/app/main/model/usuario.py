
from .. import db, flask_bcrypt
import datetime
from app.main.model.blacklist import BlacklistToken
from ..config import key
import jwt
from typing import Union
from .. model.perfil import Perfil

class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(128), nullable=True)
    login = db.Column(db.String(128), unique=True, nullable=False)
    senhaHash = db.Column(db.String(100))
    ativo = db.Column(db.Boolean,default=True)
    perfil_id = db.Column(db.Integer, db.ForeignKey('perfil.id'))
    perfil = db.relationship('Perfil', backref='perfil2')

    @property
    def senha(self):
        raise AttributeError('senha: campo somente leitura')


    @senha.setter
    def senha(self, senha):
        self.senhaHash = flask_bcrypt.generate_password_hash(senha).decode('utf-8')

    def check_senha(self, senha: str) -> bool:
        return flask_bcrypt.check_password_hash(self.senhaHash, senha)


    @staticmethod
    def encode_auth_token(user_id: int, user_name:str, user_login:str) -> bytes:
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'uid': user_id,
                'name': user_name,
                'login': user_login
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token: str) -> Union[str, int]:
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key, algorithms='HS256')
            
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['uid']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return "<Usuario '{}'>".format(self.login)
