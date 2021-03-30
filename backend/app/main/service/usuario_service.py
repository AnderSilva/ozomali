import uuid
import datetime

from app.main import db
from app.main.model.usuario import Usuario
from typing import Dict, Tuple


def save_new_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    usuario = Usuario.query.filter(
            Usuario.login == data['login']        
    ).first()
    if not usuario:
        novo_usuario = Usuario(            
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
            'message': 'login já existe.',
        }
        return response_object, 409


def update_user(usuario: Usuario,data):    
    if data:
        update_changes(usuario,data)        
        response_object = {
            'status': 'success',
            'message': 'Usuário atualizado com sucesso.'            
        }
        return response_object, 404 #usuario para retornar o objeto
    else:
        response_object = {
            'status': 'Falha',
            'message': 'Payload vazio, check e tente novamente.',
        }
        return response_object, 404

def get_all_users(ativo=False):    
    return Usuario.query.filter_by(ativo=ativo).all()


def get_a_user(id):
    return Usuario.query.filter_by(id=id).first()

def get_some_user(login):    
    return Usuario.query \
    .filter(
        Usuario.login \
        .like( '%{}%'.format(login) )
    ).all()


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
    usuario.login = data.get('nome' , usuario.nome)
    usuario.senha = data.get('senha', usuario.senha_hash)
    usuario.ativo = data.get('ativo', usuario.ativo)
    db.session.commit()