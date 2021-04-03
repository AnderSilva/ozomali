import uuid
import datetime

from app.main import db
from app.main.model.preco import Preco
from typing import Dict, Tuple


def save_new_price(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    preco = Preco.query.filter(
            Preco.login == data['login']        
    ).first()
    if not preco:
        novo_preco = Preco(            
            login=data['login'],
            senha=data['senha'],
        )
        save_changes(novo_preco)
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


def update_price(preco: Preco,data):    
    if data:
        update_changes(preco,data)        
        response_object = {
            'status': 'success',
            'message': 'Usuário atualizado com sucesso.'            
        }
        return response_object, 404 #preco para retornar o objeto
    else:
        response_object = {
            'status': 'Falha',
            'message': 'Payload vazio, check e tente novamente.',
        }
        return response_object, 404

def get_all_prices(ativo=False):    
    return Preco.query.filter_by(ativo=ativo).all()


def get_a_price(id):
    return Preco.query.filter_by(id=id).first()

def get_some_price(login):    
    return Preco.query \
    .filter(
        Preco.login \
        .like( '%{}%'.format(login) )
    ).all()

def save_changes(data: Preco) -> None:
    db.session.add(data)
    db.session.commit()

def update_changes(preco: Preco, data) -> None:
    preco.login = data.get('login' , preco.login)
    preco.senha = data.get('senha', preco.senha_hash)
    preco.ativo = data.get('ativo', preco.ativo)
    db.session.commit()