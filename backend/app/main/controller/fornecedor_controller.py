from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required, token_required
from ..util.dto import FornecedorDto
from ..service.fornecedor_service import *
from typing import Dict, Tuple

api = FornecedorDto.api
_fornecedorinsert = FornecedorDto.fornecedorinsert
_fornecedorlista = FornecedorDto.fornecedorlista
_fornecedorupdate = FornecedorDto.fornecedorupdate
_fornecedorupdateRetorno = FornecedorDto.fornecedorupdateRetorno

@api.route('') #,'/')
class FornecedorAPI(Resource):

    @api.doc('lista os registros de fornecedores')
    @api.doc(security='apikey')
    @token_required
    @api.marshal_list_with(_fornecedorlista, envelope='data')
    def get(self,ativo=True):
        """Lista todos fornecedores"""
        return get_all_vendors(ativo)

    @api.expect(_fornecedorinsert, validate=True)
    @api.response(201, 'Fornecedor criado com sucesso.')
    @api.doc('cria um novo fornecedor')
    @api.doc(security='apikey')
    @token_required
    def post(self) -> Tuple[Dict[str, str], int]:
        data = request.json
        return save_new_vendor(data=data)

@api.route('/<int:id>')
@api.param('id', 'Identificador do fornecedor')
@api.response(404, 'Fornecedor não encontrado.')
class Fornecedor(Resource):
    @api.doc('obter o fornecedor')
    @api.marshal_with(_fornecedorlista)
    @api.doc(security='apikey')
    @token_required
    def get(self, id):
        """Obtem informações de um fornecedor com base no seu id"""
        fornecedor = get_a_vendor('id',id)
        if not fornecedor:
            api.abort(404)
        else:
            return fornecedor

    
    @api.doc('Atualiza um fornecedor',responses={
        200: 'Sucesso',
        400: 'Erro na Atualização',
        404: 'Fornecedor não encontrado'
    })
    @api.expect(_fornecedorupdate, validate=True)
    @api.response(201, 'Fornecedor atualizado com sucesso.')
    @api.marshal_with(_fornecedorupdateRetorno)
    @api.doc(security='apikey')
    @admin_token_required
    def patch(self,id):
        """Atualiza um fornecedor  Obs: para inativar, coloque 'ativo': false """

        fornecedor = get_a_vendor('id',id)
        data = request.json
        if not fornecedor:
            api.abort(404, 'Fornecedor não encontrado.')
        if not data:
            api.abort(400, 'Payload vazio.')
                
        return update_vendor(fornecedor,data=data)

@api.route('/<string:campo>/<string:valor>')
@api.response(404, 'Nenhum fornecedor foi encontrado.')
class Fornecedor(Resource):    
    @api.marshal_with(_fornecedorlista, envelope='data')
    @api.doc(security='apikey')
    @token_required
    def get(self, campo, valor):
        """Lista de fornecedores filtrados por campo/valor"""
        fornecedor = get_a_vendor(campo,valor)
        if not fornecedor:
            api.abort(404, 'Nenhum fornecedor foi encontrado.')
        else:
            return fornecedor