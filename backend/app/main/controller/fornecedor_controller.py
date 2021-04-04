from flask import request
from flask_restx import Resource

# from app.main.util.decorator import admin_token_required
from ..util.dto import FornecedorDto
from ..service.fornecedor_service import * 
from typing import Dict, Tuple

api = FornecedorDto.api
_fornecedorinsert = FornecedorDto.fornecedorinsert
_fornecedorlista = FornecedorDto.fornecedorlista
_fornecedorupdate = FornecedorDto.fornecedorupdate

@api.route('') #,'/')
class FornecedorAPI(Resource):

    @api.doc('lista os registros de fornecedores')
    # @admin_token_required
    @api.marshal_list_with(_fornecedorlista, envelope='data')
    def get(self,ativo=True):
        """Lista todos fornecedores"""
        return get_all_vendors(ativo)

    @api.expect(_fornecedorinsert, validate=True)
    @api.response(201, 'Fornecedor criado com sucesso.')
    @api.doc('cria um novo fornecedor')
    def post(self) -> Tuple[Dict[str, str], int]:        
        data = request.json
        return save_new_vendor(data=data)

@api.route('/<int:id>')
@api.param('id', 'Identificador do fornecedor')
@api.response(404, 'Fornecedor não encontrado.')
class Fornecedor(Resource):
    @api.doc('obter o fornecedor')
    @api.marshal_with(_fornecedorlista)
    def get(self, id):
        """Obtem informações de um usuário com base no seu id"""
        fornecedor = get_a_vendor(id)
        if not fornecedor:
            api.abort(404)
        else:
            return fornecedor

    @api.doc('Atualiza um fornecedor')
    @api.expect(_fornecedorupdate) #, validate=True)
    @api.response(201, 'Fornecedor atualizado com sucesso.')
    #@api.marshal_with(_perfillist) para retornar o objeto
    def patch(self,id): # -> Tuple[Dict[str, str], int]:        
        """Atualiza um fornecedor  Obs: para inativar, coloque 'ativo': false """
        
        fornecedor = get_a_vendor(id)
        if not fornecedor:
            api.abort(404)
        else:
            data = request.json        
            return update_vendor(fornecedor,data=data)
            
@api.route('/inativos')
class FornecedorInvativos(Resource):
    @api.doc('lista fornecedores inativos')
    # @admin_token_required
    @api.marshal_list_with(_fornecedorlista, envelope='data')
    def get(self,ativo=False):
        """Lista todos os fornecedores inativos"""
        return get_all_vendors(ativo)
