import uuid
import datetime

from app.main import db
from app.main.model.movimentacao import Movimentacao
from app.main.model.usuario import Usuario
from app.main.model.produto import Produto
from app.main.model.authenticate import Authenticate
from app.main.model.preco import Preco
from typing import Dict, Tuple
from ..service.usuario_service import get_a_user
from ..service.produto_service import get_a_product
from ..service.preco_service import get_active_price

def save_new_moviment(data: Dict[str, str], authenticate:Authenticate) -> Tuple[Dict[str, str], int]:
    
    #Validacao dos ids
    produto = get_a_product('id', data.get('produto_id', 0))
    if not produto:
        response_object = {
            'status': 'Falha',
            'message': 'Id produto inválido.',
        }
        return response_object, 400

    #Validando a movimentacao
    msg = Validation(data)
    if msg:
        response_object = {
            'status': 'Falha',
            'message': msg,
        }
        return response_object, 400

    precoTotal = data.get('preco_total', 0)
    precoUnitatio = precoTotal/data['quantidade']
    #busca preco venda
    if data['tipo_movimentacao'] == 'S':
        preco = get_active_price(produto_id=produto.id)
        if not preco:
            response_object = {
                'status': 'Falha',
                'message': 'Produto não tem preco ativo, informe o preço no sistema.',
            }
            return response_object, 400
        precoTotal = preco.preco_venda * data['quantidade']
        precoUnitatio = preco.preco_venda

    #criando a movimentacao
    nova_mov = Movimentacao(
            preco_total=precoTotal,
            quantidade=data['quantidade'],
            local_estoque=data['local_estoque'],
            tipo_movimentacao=data['tipo_movimentacao'],
            data_movimentacao=datetime.datetime.today(),
            ativo=True,
            usuario_id=authenticate.uid,
            produto_id=produto.id,
        )
    save_changes(nova_mov)
    response_object = {
            'status': 'success',
            'message': 'Movimentacao registrado com sucesso.',
            'preco_total': precoTotal,
            'preco_unitario': precoUnitatio,
            'id': nova_mov.id
        }
    return response_object, 201    

def Validation(data: Dict[str, str])-> str:
    if data['tipo_movimentacao'] not in ('E', 'S'):        
        return 'tipo_movimentacao - Informe a LETRA "E" para Entrada ou "S" para Saida.'
    if data['tipo_movimentacao'] =='E' :
        if data.get('preco_total',0) == 0:
            return 'preco_total deve ser informado quando for entrada no estoque.'
        if data['preco_total'] <= 0:
            return 'preco_total deve ser maior que zero.'
    if data['quantidade'] <= 0:
        return 'quantidade deve ser maior que zero.'
    if not data['local_estoque'].strip():        
        return 'local_estoque deve ser informado.'    
    qtde = get_net_by_product(data['produto_id'], True).quantidade
    if data['tipo_movimentacao'] == 'S' and qtde < data['quantidade']:
        return 'quantidade - Quantidade de produto insuficiente. Estoque tem {}.'.format(qtde)
    return ""

def save_changes(data: Movimentacao) -> None:
    db.session.add(data)
    db.session.commit()

def get_all_moviments(ativo=False):
    return Movimentacao.query.filter_by(ativo=ativo).all()

def get_all_moviments_by_product(produto_id, ativo=False):
    return Movimentacao.query.filter_by(ativo=ativo, produto_id=produto_id).all()

def get_net_by_product(produto_id, ativo=False)-> Movimentacao:
    movs = Movimentacao.query.filter_by(ativo=ativo, produto_id=produto_id).all()
    qtde = 0
    for mov in movs:
        if mov.tipo_movimentacao == 'E':
            qtde += mov.quantidade
        else:
            qtde -= mov.quantidade
    movimento = Movimentacao
    movimento.quantidade = qtde
    return movimento