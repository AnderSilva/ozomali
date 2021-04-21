from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required, token_required
from ..util.dto import PrecoDto
from ..service.preco_service import * 
from typing import Dict, Tuple

api = PrecoDto.api
_precoinsert = PrecoDto.precoinsert
_precolista = PrecoDto.precolista
_precoproduto = PrecoDto.precoproduto

@api.route('') #,'/')
class PrecoAPI(Resource):
    @api.doc('lista os registros de fornecedores')
    @api.doc(security='apikey')
    @token_required
    @api.marshal_list_with(_precolista, envelope='data')
    def get(self,ativo=True):
        """Lista todos preços"""
        return get_all_prices(ativo)

    @api.expect(_precoinsert, validate=True)
    @api.response(201, 'Preço criado com sucesso.')
    @api.doc('cria um novo preço')
    @api.doc(security='apikey')
    @token_required
    def post(self) -> Tuple[Dict[str, str], int]:        
        data = request.json
        return save_new_price(data=data)

@api.route('/inativos')
class PrecoInativos(Resource):
    @api.doc('lista preços inativos')
    @api.doc(security='apikey')
    @token_required
    @api.marshal_list_with(_precolista, envelope='data')
    def get(self,ativo=False):
        """Lista todos preços inativos"""
        return get_all_prices(ativo)


@api.route('/<int:id>')
@api.param('id', 'Identificador do preço')
@api.response(404, 'Preço não encontrado.')
class Preco(Resource):
    @api.doc('obter preço')
    @api.marshal_with(_precolista)
    @api.doc(security='apikey')
    @token_required
    def get(self, id):
        """Obtem informações de um preço com base no seu id"""
        preco = get_a_price(id)
        if not preco:
            api.abort(404)
        else:
            return preco

@api.route('/produto/<int:id>')
@api.param('id', 'Identificador do produto')
@api.response(404, 'Preço não encontrado.')
class Preco(Resource):
    @api.doc('obter preço')
    @api.marshal_with(_precoproduto)
    @api.doc(security='apikey')
    @token_required
    def get(self, id):
        """Obtem informações de um preço de determinado produto"""        
        return get_some_price(id)
        