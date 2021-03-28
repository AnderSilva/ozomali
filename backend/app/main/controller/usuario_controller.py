from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required
from ..util.dto import UserDto
from ..service.user_service import * 
from typing import Dict, Tuple

api = UserDto.api
_userinsert = UserDto.userinsert
_userlist = UserDto.userlist
_userupdate = UserDto.userupdate


@api.route('') #,'/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    # @admin_token_required
    @api.marshal_list_with(_userlist, envelope='data')
    def get(self,ativo=True):
        """Lista todos usuários"""
        return get_all_users(ativo)

    @api.expect(_userinsert, validate=True)
    @api.response(201, 'Usuário criado com sucesso.')
    @api.doc('cria um novo usuário')
    def post(self) -> Tuple[Dict[str, str], int]:        
        data = request.json
        return save_new_user(data=data)

@api.route('/inativos')
class UserList(Resource):
    @api.doc('list_of_inactive_registered_users')
    # @admin_token_required
    @api.marshal_list_with(_userlist, envelope='data')
    def get(self,ativo=False):
        """Lista todos usuários inativos"""
        return get_all_users(ativo)


@api.route('/<int:id>')
@api.param('id', 'Identificador do usuário')
@api.response(404, 'Usuário não encontrado.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_userlist)
    def get(self, id):
        """Obtem informações de um usuário com base no seu id"""
        user = get_a_user(id)
        if not user:
            api.abort(404)
        else:
            return user

    @api.expect(_userupdate, validate=True)
    @api.response(201, 'Usuário atualizado com sucesso.')
    @api.doc('Atualiza um usuário')
    def put(self,id) -> Tuple[Dict[str, str], int]:        
        """Atualiza um usuário  Obs: para inativar, coloque 'ativo': false """
        data = request.json        
        return update_user(id=id,data=data)

@api.route('/<login>')
@api.param('login', 'parte do nome ou login do usuário')
@api.response(404, 'Usuário não encontrado.')
class User(Resource):
    @api.doc('get a user based on login')
    @api.marshal_with(_userlist)
    def get(self, login):
        """Obtem informações de um usuário com base no seu login"""
        user = get_some_user(login)
        if not user:
            api.abort(404)
        else:
            return user
