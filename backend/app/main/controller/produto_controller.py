from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required
from ..util.dto import ProdutoDto
from ..service.produto_service import save_new_product, get_all_products, get_a_product, get_some_product
from typing import Dict, Tuple

api = ProdutoDto.api
_produto = ProdutoDto.produto


@api.route('/')
class ProdutoList(Resource):
    @api.doc('lista_de_produtos_registrados')
    # @admin_token_required
    @api.marshal_list_with(_produto, envelope='data')
    def get(self):
        """Lista todos produtos"""
        return get_all_products()

    @api.expect(_produto, validate=True)
    @api.response(201, 'Produto criado com sucesso.')
    @api.doc('cria um novo produto')
    def post(self) -> Tuple[Dict[str, str], int]:        
        data = request.json
        return save_new_product(data=data)


@api.route('/id')
@api.param('id', 'Identificador do produto')
@api.response(404, 'Produto não encontrado.')
class Produto(Resource):
    @api.doc('get a produto')
    @api.marshal_with(_produto)
    def get(self, id):
        """Obtem informações de um produto com base no seu id"""
        produto = get_a_product(id)
        if not produto:
            api.abort(404)
        else:
            return produto



