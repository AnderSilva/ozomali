from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required, token_required
from ..util.dto import MovimentacaoDto
from ..service.movimentacao_service import * 
from ..service.movimentacao_report_service import movimentacao_report_by_periodo, movimento_validacao
from typing import Dict, Tuple

api = MovimentacaoDto.api
_movimentacaoinsert = MovimentacaoDto.movimentacaoinsert
_movimentacao_lista = MovimentacaoDto.movimentacao_lista
_movimentacao_saldo = MovimentacaoDto.movimentacao_saldo
_movimentacao_report = MovimentacaoDto.movimentacao_report
_movimentacao_report_filtro = MovimentacaoDto.movimentacao_report_filtro

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
        return save_new_moviment(data=data, authenticate=self.authenticate)

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

@api.route('/report')
class ReportMovimentacao(Resource):
    @api.doc('report_movimentacao')
    @api.doc(security='apikey')
    @token_required
    @api.expect(_movimentacao_report_filtro, validate=True)
    @api.marshal_list_with(_movimentacao_report, envelope='data')
    def post(self,ativo=True):
        """Analise de movimentacao"""
        data = request.json
        validation = movimento_validacao(data)
        print(validation[1])
        if validation[1] != 200:
            return validation
        
        return movimentacao_report_by_periodo(data=data)