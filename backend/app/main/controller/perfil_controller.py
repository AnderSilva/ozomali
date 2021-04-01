from flask import request
from flask_restx import Resource

# from app.main.util.decorator import admin_token_required
from ..util.dto import PerfilDto
from ..service.perfil_service import * 
from typing import Dict, Tuple

api = PerfilDto.api
_perfil = PerfilDto.perfil

@api.route('') #,'/')
class PerfilList(Resource):
    @api.doc('list_of_registered_users')
    # @admin_token_required
    @api.marshal_list_with(_perfil, envelope='data')
    def get(self,ativo=True):
        """Lista todos usuários"""
        return get_all_profiles(ativo)

    @api.expect(_perfil, validate=True)
    @api.response(201, 'Perfil criado com sucesso.')
    @api.doc('cria um novo perfil')
    def post(self) -> Tuple[Dict[str, str], int]:        
        data = request.json
        return save_new_profile(data=data)

@api.route('/inativos')
class PerfilListas(Resource):
    @api.doc('list_of_inactive_registered_users')
    # @admin_token_required
    @api.marshal_list_with(_perfil, envelope='data')
    def get(self,ativo=False):
        """Lista todos usuários inativos"""
        return get_all_users(ativo)


@api.route('/<int:id>')
@api.param('id', 'Identificador do usuário')
@api.response(404, 'Usuário não encontrado.')
class Perfil(Resource):
    @api.doc('get a profile')
    @api.marshal_with(_perfil)
    def get(self, id):
        """Obtem informações de um usuário com base no seu id"""
        perfil = get_a_user(id)
        if not perfil:
            api.abort(404)
        else:
            return perfil


    @api.doc('Atualiza um usuário')
    @api.expect(_perfil) #, validate=True)
    @api.response(201, 'Usuário atualizado com sucesso.')
    #@api.marshal_with(_perfillist) para retornar o objeto
    def patch(self,id): # -> Tuple[Dict[str, str], int]:        
        """Atualiza um usuário  Obs: para inativar, coloque 'ativo': false """
        
        perfil = get_a_user(id)
        if not perfil:
            api.abort(404)
        else:
            data = request.json        
            return update_user(perfil,data=data)


@api.route('/<string:login>')
@api.param('login', 'parte do login do usuário')
@api.response(404, 'login não encontrado.')
class Perfil(Resource):
    @api.doc('obtem perfil com base no login')
    @api.marshal_with(_perfil)
    def get(self, login):
        """Lista de usuário filtrados por login"""
        perfil = get_some_user(login)
        if not perfil:
            api.abort(404)
        else:
            return perfil
