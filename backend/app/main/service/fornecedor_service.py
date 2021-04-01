import uuid
import datetime

from app.main import db
from app.main.model.fornecedor import Fornecedor
from typing import Dict, Tuple


def save_new_fornecedor(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    fornecedor = Fornecedor.query.filter(
        db.or_(
             Fornecedor.nome  == data['nome']
            ,Fornecedor.login == data['login']
        )
    ).first()
    if not fornecedor:
        novo_fornecedor = Fornecedor(            
            login=data['login'],
            senha=data['senha'],
        )
        save_changes(novo_fornecedor)
        response_object = {
            'status': 'success',
            'message': 'Fornecedor registrado com sucesso.',
        }
        return response_object, 201
        # return generate_token(new_user)
    else:
        response_object = {
            'status': 'Falha',
            'message': 'nome/login já existe.',
        }
        return response_object, 409


def update_user(fornecedor: Fornecedor,data):    
    if data:
        update_changes(fornecedor,data)        
        response_object = {
            'status': 'success',
            'message': 'Usuário atualizado com sucesso.'            
        }
        return response_object, 404 #fornecedor para retornar o objeto
    else:
        response_object = {
            'status': 'Falha',
            'message': 'Payload vazio, check e tente novamente.',
        }
        return response_object, 404

def get_all_users(ativo=False):    
    return Fornecedor.query.filter_by(ativo=ativo).all()


def get_a_user(id):
    return Fornecedor.query.filter_by(id=id).first()

def get_some_user(login):
    return Fornecedor.query \
    .filter(
        Fornecedor.login \
        .like( '%{}%'.format(login) )
    ).all()


def generate_token(user: Fornecedor) -> Tuple[Dict[str, str], int]:
    try:
        # generate the auth token
        auth_token = Fornecedor.encode_auth_token(fornecedor.id)
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


def save_changes(data: Fornecedor) -> None:
    db.session.add(data)
    db.session.commit()

def update_changes(fornecedor: Fornecedor, data) -> None:
    fornecedor.nome  = data['nome']  if data['nome']  !=None else fornecedor.nome
    fornecedor.senha = data['senha'] if data['senha'] !=None else fornecedor.senha
    fornecedor.ativo = data['ativo'] if data['ativo'] !=None else fornecedor.ativo
    db.session.commit()