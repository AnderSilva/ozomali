from flask import request
from flask_restx import Resource

# from app.main.util.decorator import admin_token_required
from ..util.dto import PrecoDto
from ..service.preco_service import * 
from typing import Dict, Tuple

api = PrecoDto.api
_preco = PrecoDto.preco

@api.route('') #,'/')
class PrecoList(Resource):
    @api.doc('list_of_registered_users')
    # @admin_token_required
    @api.marshal_list_with(_preco, envelope='data')
    def get(self,ativo=True):
        """Lista todos usuários"""
        return get_all_prices(ativo)

    @api.expect(_preco, validate=True)
    @api.response(201, 'Usuário criado com sucesso.')
    @api.doc('cria um novo usuário')
    def post(self) -> Tuple[Dict[str, str], int]:        
        data = request.json
        return save_new_price(data=data)

@api.route('/inativos')
class PrecoListas(Resource):
    @api.doc('list_of_inactive_registered_users')
    # @admin_token_required
    @api.marshal_list_with(_preco, envelope='data')
    def get(self,ativo=False):
        """Lista todos usuários inativos"""
        return get_all_prices(ativo)


@api.route('/<int:id>')
@api.param('id', 'Identificador do usuário')
@api.response(404, 'Usuário não encontrado.')
class Preco(Resource):
    @api.doc('get a user')
    @api.marshal_with(_preco)
    def get(self, id):
        """Obtem informações de um usuário com base no seu id"""
        preco = get_a_price(id)
        if not preco:
            api.abort(404)
        else:
            return preco


    @api.doc('Atualiza um usuário')
    @api.expect(_preco) #, validate=True)
    @api.response(201, 'Usuário atualizado com sucesso.')
    #@api.marshal_with(_precolist) para retornar o objeto
    def patch(self,id): # -> Tuple[Dict[str, str], int]:        
        """Atualiza um usuário  Obs: para inativar, coloque 'ativo': false """
        
        preco = get_a_price(id)
        if not preco:
            api.abort(404)
        else:
            data = request.json        
            return update_price(preco,data=data)


@api.route('/<string:login>')
@api.param('login', 'parte do login do usuário')
@api.response(404, 'login não encontrado.')
class Preco(Resource):
    @api.doc('obtem preco com base no login')
    @api.marshal_with(_preco)
    def get(self, login):
        """Lista de usuário filtrados por login"""
        preco = get_some_price(login)
        if not preco:
            api.abort(404)
        else:
            return preco
