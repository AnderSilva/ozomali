from flask import request
from flask_restx import Resource

# from app.main.util.decorator import admin_token_required
from ..util.dto import PerfilDto
from ..service.perfil_service import * 
from typing import Dict, Tuple

api = PerfilDto.api
_perfil = PerfilDto.perfil
_perfilinsert = PerfilDto.perfilinsert
_perfilupdate = PerfilDto.perfilupdate

@api.route('') #,'/')
class PerfilList(Resource):
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_perfil, envelope='data')
    def get(self,ativo=True):
        """Lista todos perfis de usuário"""
        return get_all_profiles(ativo)

    @api.expect(_perfilinsert, validate=True)
    @api.response(201, 'Perfil criado com sucesso.')
    @api.doc('cria um novo perfil')
    def post(self) -> Tuple[Dict[str, str], int]:        
        data = request.json
        return save_new_profile(data=data)

@api.route('/inativos')
class PerfilListas(Resource):
    @api.doc('list_of_inactive_registered_users')
    @api.marshal_list_with(_perfil, envelope='data')
    def get(self,ativo=False):
        """Lista todos Perfis inativos"""
        return get_all_profiles(ativo)


@api.route('/<int:id>')
@api.param('id', 'Identificador do Perfil')
@api.response(404, 'Perfil não encontrado.')
class Perfil(Resource):
    @api.doc('get a profile')
    @api.marshal_with(_perfil)
    def get(self, id):
        """Obtem informações de um perfil com base no seu id"""
        perfil = get_a_profile(id)
        if not perfil:
            api.abort(404)
        else:
            return perfil


    @api.doc('Atualiza um Perfil')
    @api.expect(_perfilupdate)
    @api.response(201, 'Perfil atualizado com sucesso.')
    @api.marshal_with(_perfil)
    def patch(self,id): # -> Tuple[Dict[str, str], int]:        
        """Atualiza um Perfil  Obs: para inativar, coloque 'ativo': false """
        
        perfil = get_a_profile(id)
        data = request.json
        if not perfil:
            api.abort(404, 'Perfil não encontrado.')
        if not data:
            api.abort(400, 'Payload vazio.')

        return update_profile(perfil,data=data)
            