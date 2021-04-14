import uuid
import datetime

from app.main import db
from app.main.model import unaccent
from app.main.model.usuario import Usuario
from app.main.model.perfil import Perfil
from typing import Dict, Tuple


def save_new_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    usuario = Usuario.query.filter(
            db.or_(Usuario.login == data['login']
                  ,Usuario.nome == data['nome'])
    ).first()
    perfil = Perfil.query.filter_by(id=data['perfil_id'], ativo=True).first()
    if not perfil:
        response_object = {
            'status': 'Falha',
            'message': 'perfil não encontrado ou inativo.',
        }
        return response_object, 404

    if not usuario:
        novo_usuario = Usuario(
            login=data['login'],
            senha=data['senha'],
            nome=data['nome'],
            perfil_id=data['perfil_id'],
        )
        save_changes(novo_usuario)
        response_object = {
            'status': 'success',
            'message': 'Usuário registrado com sucesso.',
            'id' : novo_usuario.id,
        }
        return response_object, 201
        # return generate_token(new_user)
    else:
        response_object = {
            'status': 'Falha',
            'message': 'login / nome já existente.',
        }
        return response_object, 409


def update_user(usuario: Usuario,data):
    update_changes(usuario,data)
    return usuario


def get_all_users(ativo=False):
    usuarios = Usuario.query.filter_by(ativo=ativo)
    return usuarios.join(Perfil).all()
    #return Usuario.query.filter_by(ativo=ativo).all()


def get_a_user(tipo, id):
    item = '%{}%'.format(id)

    if tipo=='id':
        return Usuario.query.filter_by(id=id).first()
    
    if tipo=='login':
        return Usuario.query.filter(
            unaccent(Usuario.login)
            .ilike( item )
        ).all()

    if tipo=='nome':
        return Usuario.query.filter(
            unaccent(Usuario.nome)
            .ilike( item )
        ).all()

    if tipo=='perfil_id':
        return Usuario.query.filter_by(perfil_id=id).all()
    
    if tipo=='ativo':
        return Usuario.query.filter_by(ativo=id).all()


def get_some_user(login):
    return Usuario.query \
    .filter(
        unaccent(Usuario.login) \
        .ilike( '%{}%'.format(login) )
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
    usuario.login = data.get('login' , usuario.login)
    usuario.nome = data.get('nome' , usuario.nome)
    if data.get('senha', 0) != 0:
        usuario.senha = data['senha']
    usuario.ativo = data.get('ativo', usuario.ativo)
    db.session.commit()
