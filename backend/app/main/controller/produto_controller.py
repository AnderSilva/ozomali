from flask import request
from flask_restx import Resource

from ..util.dto import ProdutoDto
from ..service.produto_service import *
from typing import Dict, Tuple
from app.main.util.decorator import admin_token_required, token_required

api = ProdutoDto.api
_produtolist = ProdutoDto.produtolist
_produtoinsert = ProdutoDto.produtoinsert
_produtoupdate = ProdutoDto.produtoupdate
_produtoupdateretorno = ProdutoDto.produtoupdateretorno
_produtolistPesquisa = ProdutoDto.produtolistPesquisa


@api.route('')
class ProdutoLista(Resource):
    @api.doc('lista_de_produtos_registrados')
    @api.doc(security='apikey')
    @token_required
    @api.marshal_list_with(_produtolist, envelope='data')
    def get(self):
        """Lista todos produtos"""
        return get_all_products()

    @api.expect(_produtoinsert, validate=True)
    @api.doc('Cria um novo Produto',responses={
        200: 'Criado com Sucesso.',
        404: 'Fornecedor não encontrado.',
        409: 'Produto já existente.'
    })
    @api.doc(security='apikey')
    @token_required
    def post(self) -> Tuple[Dict[str, str], int]:
        data = request.json
        return save_new_product(data=data, authenticate=self.authenticate)

@api.route('/pesquisa')
class ProdutoListaPesquisa(Resource):
    @api.doc('lista_de_produtos_registrados_pesquisa')
    @api.doc(security='apikey')
    @token_required
    @api.expect(_produtolistPesquisa, validate=True)
    @api.marshal_list_with(_produtolist, envelope='data')
    def post(self,ativo=True):
        """Lista todos produtos pesquisados"""
        data = request.json
        return get_search_products(data=data)

@api.route('/<int:id>')
@api.param('id', 'Identificador do produto')
@api.response(404, 'Produto não encontrado.')
class ProdutoID(Resource):
    @api.doc('get a produto')
    @api.marshal_with(_produtolist)
    @api.doc(security='apikey')
    @token_required
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
    @api.marshal_with(_produtoupdateretorno)
    @api.doc(security='apikey')
    @token_required
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

        return update_product(produto,data=data, authenticate=self.authenticate)


@api.route('/<string:campo>/<string:valor>')
@api.doc('Atualiza um Produto',responses={
    200: 'Lista dos Produtos encontrados.',
    404: 'Nenhum produto encontrado com o filtro informado.'
})
class ProdutoCampoValor(Resource):    
    @api.marshal_with(_produtolist, envelope='data')
    @api.doc(security='apikey')
    @token_required
    def get(self, campo, valor):
        """Lista de Produtos filtrados por campo/valor"""
        produtos = get_a_product(campo,valor)
        if not produtos:
            api.abort(404, 'Nenhum produto foi encontrado.')
        else:
            return produtos