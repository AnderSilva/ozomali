from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required, token_required
from ..util.dto import MovimentacaoDto
from ..service.movimentacao_service import * 
from typing import Dict, Tuple

api = MovimentacaoDto.api
_movimentacaoinsert = MovimentacaoDto.movimentacaoinsert
_movimentacao_lista = MovimentacaoDto.movimentacao_lista
_movimentacao_saldo = MovimentacaoDto.movimentacao_saldo

@api.route('') #,'/')
class MovimentacaoRoute(Resource):    

    @api.doc('lista todas as movimentacoes')
    @api.marshal_list_with(_movimentacao_lista, envelope='data')
    @api.doc(security='apikey')
    @token_required
    def get(self,ativo=True):
        """Lista todas as movimentacoes"""
        return get_all_moviments(ativo)

    @api.expect(_movimentacaoinsert, validate=True)
    @api.response(201, 'Movimentacao criado com sucesso.')
    @api.doc('cria um novo movimento de estoque')
    @api.doc(security='apikey')
    @token_required
    def post(self) -> Tuple[Dict[str, str], int]:        
        data = request.json
        return save_new_moviment(data=data)

@api.route('/<int:produto_id>')
class MovimentacaoPorProduto(Resource):
    @api.doc('lista todas as movimentacoes por produto')
    @api.marshal_list_with(_movimentacao_lista, envelope='data')
    @api.doc(security='apikey')
    @token_required
    def get(self, produto_id):
        """Lista todas as movimentacoes por produto"""
        return get_all_moviments_by_product(produto_id = produto_id, ativo=True)

@api.route('/saldo/<int:produto_id>')
class SaldoMovimentacaoPorProduto(Resource):
    @api.doc('informa o saldo no estoque por produto')
    @api.marshal_list_with(_movimentacao_saldo, envelope='data')
    @api.doc(security='apikey')
    @token_required
    def get(self, produto_id):
        """Informa o saldo no estoque por produto"""
        return get_net_by_product(produto_id = produto_id, ativo=True)