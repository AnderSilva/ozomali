from flask import request
from flask_restx import Resource

# from app.main.util.decorator import admin_token_required
from ..util.dto import FornecedorDto
from ..service.fornecedor_service import * 
from typing import Dict, Tuple

api = FornecedorDto.api
_fornecedor = FornecedorDto.fornecedor

@api.route('') #,'/')
class FornecedorList(Resource):
    @api.doc('list_of_registered_users')
    # @admin_token_required
    @api.marshal_list_with(_fornecedor, envelope='data')
    def get(self,ativo=True):
        """Lista todos usuários"""
        return get_all_users(ativo)

    @api.expect(_fornecedor, validate=True)
    @api.response(201, 'Usuário criado com sucesso.')
    @api.doc('cria um novo usuário')
    def post(self) -> Tuple[Dict[str, str], int]:        
        data = request.json
        return save_new_user(data=data)

@api.route('/inativos')
class FornecedorListas(Resource):
    @api.doc('list_of_inactive_registered_users')
    # @admin_token_required
    @api.marshal_list_with(_fornecedor, envelope='data')
    def get(self,ativo=False):
        """Lista todos usuários inativos"""
        return get_all_users(ativo)


@api.route('/<int:id>')
@api.param('id', 'Identificador do usuário')
@api.response(404, 'Usuário não encontrado.')
class Fornecedor(Resource):
    @api.doc('get a user')
    @api.marshal_with(_fornecedor)
    def get(self, id):
        """Obtem informações de um usuário com base no seu id"""
        fornecedor = get_a_user(id)
        if not fornecedor:
            api.abort(404)
        else:
            return fornecedor


    @api.doc('Atualiza um usuário')
    @api.expect(_fornecedor) #, validate=True)
    @api.response(201, 'Usuário atualizado com sucesso.')
    #@api.marshal_with(_fornecedor) para retornar o objeto
    def patch(self,id): # -> Tuple[Dict[str, str], int]:        
        """Atualiza um usuário  Obs: para inativar, coloque 'ativo': false """
        
        fornecedor = get_a_user(id)
        if not fornecedor:
            api.abort(404)
        else:
            data = request.json        
            return update_user(fornecedor,data=data)


@api.route('/<string:login>')
@api.param('login', 'parte do login do usuário')
@api.response(404, 'login não encontrado.')
class Fornecedor(Resource):
    @api.doc('obtem fornecedor com base no login')
    @api.marshal_with(_fornecedor)
    def get(self, login):
        """Lista de usuário filtrados por login"""
        fornecedor = get_some_user(login)
        if not fornecedor:
            api.abort(404)
        else:
            return fornecedor
