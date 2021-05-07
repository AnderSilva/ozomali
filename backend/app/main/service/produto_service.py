import uuid
import datetime

from app.main import db
from typing import Dict, Tuple
from app.main.model import unaccent
from app.main.model.produto import Produto
from app.main.model.fornecedor import Fornecedor


def save_new_product(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    produto = Produto.query.filter(
            db.or_(Produto.nome == data['nome']
                  ,Produto.codigo_barra == data['codigo_barra'])
    ).first()

    fornecedor  = Fornecedor.query.filter_by(id=data['fornecedor_id']).first()

    if not fornecedor:
        response_object = {
            'status': 'Falha',
            'message': 'Fornecedor não encontrado.',
        }
        return response_object, 404

    if not produto:
        novo_produto = Produto(
            nome=data['nome'],
            codigo_barra=data['codigo_barra'],
            fornecedor_id=data['fornecedor_id'],
        )
        save_changes(novo_produto)
        response_object = {
            'status': 'success',
            'message': 'Produto registrado com sucesso.',
            'id' : novo_produto.id,
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'Falha',
            'message': 'Produto já existe. Tente novamente.',
        }
        return response_object, 409


def update_product(produto: Produto,data):
    update_changes(produto,data)
    return produto


def get_all_products(ativo=False):
    p = Produto.query.filter_by(ativo=ativo).all()    
    return p

def get_a_product(tipo, id):
    if tipo=='id':
        return Produto.query.filter_by(id=id).first()

    if tipo=='nome':
        item = '%{}%'.format(id)
        filter1 = unaccent(Produto.nome).ilike(item)
        filter2 = Produto.nome.ilike(item)
        return Produto.query.filter( db.or_(filter1,filter2) ).all()

    if tipo=='codigo_barra':
        return Produto.query.filter_by(id=id).all()

    if tipo=='fornecedor_id':
        return Produto.query.filter_by(fornecedor_id=id).all()

    if tipo=='ativo':
        return Produto.query.filter_by(ativo=id).all()


def save_changes(data: Produto) -> None:
    db.session.add(data)
    db.session.commit()

def update_changes(produto: Produto, data) -> None:
    produto.nome         = data.get('nome'         , produto.nome)
    produto.codigo_barra = data.get('codigo_barra' , produto.codigo_barra)
    produto.ativo        = data.get('ativo'        , produto.ativo)
    produto.fornecedor_id= data.get('fornecedor_id', produto.fornecedor_id)

    db.session.commit()
