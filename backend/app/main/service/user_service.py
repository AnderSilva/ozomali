import uuid
import datetime

from app.main import db
from app.main.model.user import User
from typing import Dict, Tuple


def save_new_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    user = User.query.filter_by(login=data['login']).first()
    if not user:
        new_user = User(                        
            nome=data['nome'],
            login=data['login'],
            senha=data['senha'],         
        )
        save_changes(new_user)
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'Falha',
            'message': 'Usuário já existe. Logar novamente.',
        }
        return response_object, 409


def get_all_users():
    return User.query.all()


def get_a_user(id):
    return User.query.filter_by(id=id).first()


def generate_token(user: User) -> Tuple[Dict[str, str], int]:
    try:
        # generate the auth token
        auth_token = User.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Registrado com sucesso.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'falha',
            'message': 'Erro detectado. Por favor tente novamente.'
        }
        return response_object, 401


def save_changes(data: User) -> None:
    db.session.add(data)
    db.session.commit()

