import uuid
import datetime

from app.main import db
from app.main.model.usuario import Usuario
from typing import Dict, Tuple


def save_new_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    usuario = Usuario.query.filter_by(login=data['login']).first()
    if not usuario:
        novo_usuario = Usuario(
            nome=data['nome'],
            login=data['login'],
            senha=data['senha'],
        )
        save_changes(novo_usuario)
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
    usuario = Usuario.query.filter_by(id=id).first()
    if usuario:
        update_changes(usuario,data)        
        response_object = {
            'status': 'success',
            'message': 'Usuário atualizado com sucesso.',
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'Falha',
            'message': 'Usuário inexistente.',
        }
        return response_object, 404

def get_all_users(ativo=False):    
    return Usuario.query.filter_by(ativo=ativo).all()


def get_a_user(id):
    return Usuario.query.filter_by(id=id).first()

def get_some_user(login):
    item = '%{}%'.format(login)
    filter1 = Usuario.login.like(item)
    filter2 = Usuario.nome.like(item)
    return Usuario.query.filter(db.or_(filter1,filter2)).all()


def generate_token(user: Usuario) -> Tuple[Dict[str, str], int]:
    try:
        # generate the auth token
        auth_token = Usuario.encode_auth_token(usuario.id)
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


def save_changes(data: Usuario) -> None:
    db.session.add(data)
    db.session.commit()

def update_changes(usuario: Usuario, data) -> None:
    usuario.nome  = data['nome']
    usuario.senha = data['senha']
    usuario.ativo = data['ativo']
    db.session.commit()