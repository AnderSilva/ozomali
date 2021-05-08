import uuid
import datetime

from app.main import db
from app.main.model.preco import Preco
from app.main.model.usuario import Usuario
from app.main.model.produto import Produto
from typing import Dict, Tuple


def save_new_price(data: Dict[str, str], usuario_id: int) -> Tuple[Dict[str, str], int]:
    produto = Produto.query.filter(
        Produto.id == data['produto_id']
    ).first()
    if not produto:
        response_object = {
            'status': 'Falha',
            'message': 'Id produto inválido.',
        }
        return response_object, 409        
        
    preco = Preco.query.filter(
            Preco.preco_venda == data['preco_venda'],
            Preco.produto_id == data['produto_id'],
            Preco.ativo == True      
    ).first()
    if not preco:
        novo_preco = Preco(            
            preco_venda=data['preco_venda'],
            data_emissao=datetime.datetime.today(),
            ativo=True,
            usuario_id=usuario_id,
            produto_id=data['produto_id'],
        )
        save_changes(novo_preco)        
        InactiveOldPrice(novo_preco)
        response_object = {
            'status': 'success',
            'message': 'Preço registrado com sucesso.',
            'id': novo_preco.id
        }
        return response_object, 201
        # return generate_token(new_user)
    else:
        response_object = {
            'status': 'Falha',
            'message': 'Preço já existe.',
        }
        return response_object, 409

def InactiveOldPrice(data: Preco):
    preco = Preco.query.filter(            
            Preco.produto_id == data.produto_id,
            Preco.id != data.id,
            Preco.ativo == True      
    ).all()
    for t in preco:
        t.ativo = False
        update_changes(t)    


def get_all_prices(ativo=False):    
    return Preco.query.filter_by(ativo=ativo).all()

def get_a_price(id):
    return Preco.query.filter_by(id=id).first()

def get_some_price(produto_id) -> Tuple[Dict[str, str], int]:
    preco = Preco.query.filter(
        Preco.produto_id == produto_id,
        Preco.ativo == True,
    ).first()
    if not preco:
        response_object = {
            'status': 'Falha',
            'message': 'Produto não possui preço.',
        }
        return response_object, 404
    else:
        response_object = {
            'id': preco.id,
            'preco_venda': preco.preco_venda,
            'data_emissao': preco.data_emissao,
            'usuario_id': preco.usuario_id,
            'produto_id': preco.produto_id,
            'ativo': preco.ativo,
        }
        return response_object, 200

def get_active_price(produto_id):
    preco = Preco.query.filter(
        Preco.produto_id == produto_id,
        Preco.ativo == True,
    ).first()
    return preco

def save_changes(data: Preco) -> None:
    db.session.add(data)
    db.session.commit()

def update_changes(preco: Preco) -> None:    
    db.session.commit()
