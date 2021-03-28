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
        response_object = {
            'status': 'success',
            'message': 'Usuário registrado com sucesso.',
        }
        return response_object, 201
        # return generate_token(new_user)
    else:
        response_object = {
            'status': 'Falha',
            'message': 'Usuário já existe.',
        }
        return response_object, 409


def update_user(id,data):    
    user = User.query.filter_by(id=id).first()    
    user.nome  = data['nome']
    user.senha = data['senha']
    user.ativo = data['ativo']
    db.session.commit()
    response_object = {
        'status': 'success',
        'message': 'Usuário atualizado com sucesso.',
    }
    return response_object, 200

def get_all_users(ativo=False):    
    return User.query.filter_by(ativo=ativo).all()


def get_a_user(id):
    return User.query.filter_by(id=id).first()

def get_some_user(login):
    item = '%{}%'.format(login)
    filter1 = User.login.like(item)
    filter2 = User.nome.like(item)
    return User.query.filter(db.or_(filter1,filter2)).all()


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

