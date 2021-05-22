import uuid
import datetime
import unidecode

from app.main import db
from typing import Dict, Tuple
from app.main.model import unaccent
from app.main.model.produto import Produto
from app.main.model.authenticate import Authenticate
from app.main.model.preco import Preco
from app.main.model.fornecedor import Fornecedor
from app.main.service.preco_service import save_changes as save_price, InactiveOldPrice
from sqlalchemy.sql import text

def save_new_product(data: Dict[str, str], authenticate: Authenticate) -> Tuple[Dict[str, str], int]:
    if not authenticate.perfil in ('admin', 'estoque'):
        response_object = {
            'status': 'Falha',
            'message': 'Não autorizado, verifique com o administrador.',
        }
        return response_object, 400

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
        if data.get('preco_venda'):
            novo_preco = Preco(
                preco_venda=data['preco_venda'],
                data_emissao=datetime.datetime.today(),
                ativo=True,
                usuario_id=authenticate.uid,
                produto_id=novo_produto.id,
            )            
            save_price(novo_preco)            
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


def update_product(produto: Produto,data, authenticate: Authenticate) -> Tuple[Dict[str, str], int]:
    if not authenticate.perfil in ('admin', 'estoque'):
        response_object = {
            'status': 'Falha',
            'message': 'Não autorizado, verifique com o administrador.',
        }
        return response_object, 400
    update_changes(produto,data)
    if data.get('preco_venda'):
        preco = Preco.query.filter(
            Preco.preco_venda == data['preco_venda'],
            Preco.produto_id == produto.id,
            Preco.ativo == True      
        ).first()
        if not preco:
            novo_preco = Preco(
                preco_venda=data['preco_venda'],
                data_emissao=datetime.datetime.today(),
                ativo=True,
                usuario_id=authenticate.uid,
                produto_id=produto.id,
            )
            save_price(novo_preco)
            InactiveOldPrice(novo_preco)
            
    produtoUpdated = get_a_product(tipo='id',id=produto.id)
    response_object = {
            'status': 'success',
            'message': 'Produto atualizado com sucesso.',
            'id' : produtoUpdated.id,
            'nome' : produtoUpdated.nome,
            'codigo_barra' : produtoUpdated.codigo_barra,
            'fornecedor_id' : produtoUpdated.fornecedor_id,
            'preco_venda' : produtoUpdated.preco_venda,
            'saldo' : produtoUpdated.saldo,
            'ativo' : produtoUpdated.ativo,
        }
    return response_object, 200   

def get_all_products(ativo=False):
    p = Produto.query.filter_by(ativo=ativo).all()    
    return p

def get_search_products(data):
    filters = ''    
    if data.get('nome',''):
        filters += "LOWER(unaccent(produto.nome)) like '%" + unidecode.unidecode(data.get('nome','')).lower() + "%'"

    if data.get('id',0) != 0:
        if filters:
            filters += " AND "
        filters += "produto.id = " + str(data.get('id',0))

    if data.get('codigo_barra',''):
        if filters:
            filters += " AND "
        filters += "codigo_barra like '%" + data.get('codigo_barra','') + "%'"

    if data.get('ativo','') == False or data.get('ativo','')== True:
        if filters:
            filters += " AND "
        filters += "produto.ativo =" 
        filters += "'true'" if data.get('ativo','')== True else "'false'"

    if data.get('nome_fornecedor',''):
        if filters:
            filters += " AND "
        filters += "fornecedor.id in (SELECT ID FROM FORNECEDOR WHERE LOWER(unaccent(NOME)) LIKE '%" + unidecode.unidecode(data.get('nome_fornecedor','')).lower() + "%')"

    if data.get('preco_venda_ini',0)>0 or data.get('preco_venda_fin',0)>0:
        if filters:
            filters += " AND "
        subWhere = ''
        if data.get('preco_venda_ini',0)>0:
            subWhere += "p.preco_venda >= " + str(data.get('preco_venda_ini',''))
        if data.get('preco_venda_fin',0)>0:
            if subWhere:
                subWhere += ' and '
            subWhere += "p.preco_venda <= " + str(data.get('preco_venda_fin',''))
        filters += "produto.id in (SELECT produto_id FROM preco p WHERE p.ativo = 'true' and " + subWhere + ")"

    return Produto.query.join(Fornecedor).filter(text(filters)).all()

def get_a_product(tipo, id):
    if tipo=='id':
        return Produto.query.filter_by(id=id).first()

    if tipo=='nome':
        item = '%{}%'.format(id)
        filter1 = unaccent(Produto.nome).ilike(item)
        filter2 = Produto.nome.ilike(item)
        return Produto.query.filter( db.or_(filter1,filter2) ).all()

    if tipo=='codigo_barra':
        return Produto.query.filter_by(codigo_barra=id).all()

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
