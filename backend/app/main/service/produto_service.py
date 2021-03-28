import uuid
import datetime

from app.main import db
from app.main.model.produto import Produto
from typing import Dict, Tuple


def save_new_product(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    produto = Produto.query.filter_by(nome=data['nome']).first()
    if not produto:
        new_product = Produto(                        
            nome=data['nome'],
            codigoBarra=data['codigoBarra']            
        )
        save_changes(new_product)
        response_object = {
            'status': 'success',
            'message': 'Registrado com sucesso.'            
        }
        return response_object, 201        
    else:
        response_object = {
            'status': 'Falha',
            'message': 'Produto já existe. Tente novamente.',
        }
        return response_object, 409


def get_all_products():
    return Produto.query.all()


def get_a_product(id):
    return Produto.query.filter_by(id=id).first()

def get_some_product(nome):
    item = '%{}%'.format(nome)
    filter1 = Produto.nome.like(item)

    return Produto.query.filter( filter1 ).all()


def save_changes(data: Produto) -> None:
    db.session.add(data)
    db.session.commit()

