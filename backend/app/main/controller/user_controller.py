from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required
from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user
from typing import Dict, Tuple

api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    # @admin_token_required
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """Lista todos usuários"""
        return get_all_users()

    @api.expect(_user, validate=True)
    @api.response(201, 'Usuário criado com sucesso.')
    @api.doc('cria um novo usuário')
    def post(self) -> Tuple[Dict[str, str], int]:        
        data = request.json
        return save_new_user(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'Identificador do usuário')
@api.response(404, 'Usuário não encontrado.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, public_id):
        """Obtem informações de um usuário com base no seu id"""
        user = get_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user



