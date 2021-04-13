from flask import request
from flask_restx import Resource

from ..util.dto import ProdutoDto
from ..service.produto_service import *
from typing import Dict, Tuple

api = ProdutoDto.api
_produtolist = ProdutoDto.produtolist
_produtoinsert = ProdutoDto.produtoinsert
_produtoupdate = ProdutoDto.produtoupdate


@api.route('')
class ProdutoLista(Resource):
    @api.doc('lista_de_produtos_registrados')
    # @admin_token_required
    @api.marshal_list_with(_produtolist, envelope='data')
    def get(self,ativo=True):
        """Lista todos produtos"""
        return get_all_products(ativo)

    @api.expect(_produtoinsert, validate=True)
    @api.doc('Cria um novo Produto',responses={
        200: 'Criado com Sucesso.',
        404: 'Fornecedor não encontrado.',
        409: 'Produto já existente.'
    })    
    def post(self) -> Tuple[Dict[str, str], int]:
        data = request.json
        return save_new_product(data=data)


@api.route('/<int:id>')
@api.param('id', 'Identificador do produto')
@api.response(404, 'Produto não encontrado.')
class ProdutoID(Resource):
    @api.doc('get a produto')
    @api.marshal_with(_produtolist)
    def get(self, id):
        """Obtem informações de um produto com base no seu id"""
        produto = get_a_product('id',id)
        if not produto:
            api.abort(404)
        else:
            return produto


    @api.doc('Atualiza um Produto',responses={
        200: 'Atualizado com Sucesso.',
        404: 'Produto/Fornecedor não encontrado',
        400: 'Payload Vazio'
    })
    @api.expect(_produtoupdate, validate=True)    
    @api.marshal_with(_produtoupdate)
    def patch(self,id):
        """Atualiza um produto  Obs: para inativar, coloque 'ativo': false """

        produto = get_a_product('id',id)
        data = request.json
        if not produto :
            api.abort(404,'Produto não Encontrado.')
        if not data:
            api.abort(400,'Payload vazio.')
        
        if data.get('fornecedor_id', 0) != 0:
            fornecedor  = Fornecedor.query.filter_by(id=data['fornecedor_id']).first()
            if not fornecedor:
                api.abort(404,'Fornecedor Não Encontrado.')

        return update_product(produto,data=data)


@api.route('/<string:campo>/<string:valor>')
@api.doc('Atualiza um Produto',responses={
    200: 'Lista dos Produtos encontrados.',
    404: 'Nenhum produto encontrado com o filtro informado.'
})
class ProdutoCampoValor(Resource):    
    @api.marshal_with(_produtolist, envelope='data')
    def get(self, campo, valor):
        """Lista de Produtos filtrados por campo/valor"""
        produtos = get_a_product(campo,valor)
        if not produtos:
            api.abort(404, 'Nenhum produto foi encontrado.')
        else:
            return produtos