from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required, token_required
from ..util.dto import UsuarioDto
from ..service.usuario_service import * 
from typing import Dict, Tuple

api = UsuarioDto.api
_usuarioinsert = UsuarioDto.usuarioinsert
_usuariolist = UsuarioDto.usuariolist
_usuarioupdate = UsuarioDto.usuarioupdate
_usuarioListRetorno = UsuarioDto.usuarioListRetorno


@api.route('') 
class UsuarioList(Resource):
    @api.doc('list_of_registered_users')
    @api.doc(security='apikey')
    @admin_token_required
    @api.marshal_list_with(_usuariolist, envelope='data')
    def get(self,ativo=True):
        """Lista todos usuários"""
        return get_all_users(ativo)

    @api.expect(_usuarioinsert, validate=True)
    @api.doc(security='apikey')
    @admin_token_required
    @api.response(201, 'Usuário criado com sucesso.')
    @api.doc('cria um novo usuário')
    def post(self) -> Tuple[Dict[str, str], int]:        
        data = request.json
        return save_new_user(data=data)

@api.route('/<int:id>')
@api.param('id', 'Identificador do usuário')
@api.response(404, 'Usuário não encontrado.')
class UsuarioId(Resource):    
    @api.marshal_with(_usuariolist)
    @api.doc(security='apikey')
    @admin_token_required
    def get(self, id):
        """Obtem informações de um usuário com base no seu id"""
        usuario = get_a_user(id)
        if not usuario:
            api.abort(404)
        else:
            return usuario


    @api.doc('Atualiza um usuário',responses={
        200: 'Sucesso',
        400: 'Erro na Atualização',
        404: 'Perfil/Usuário não encontrado'
    })
    @api.expect(_usuarioupdate, validate=True)
    @api.response(201, 'Usuário atualizado com sucesso.')
    @api.marshal_with(_usuarioListRetorno)
    @api.doc(security='apikey')
    @admin_token_required
    def patch(self,id):
        """Atualiza um usuário  Obs: para inativar, coloque 'ativo': false """
        
        usuario = get_a_user(id)

        data = request.json
        if not usuario:
            api.abort(404, 'Usuario não encontrado.')
        if not data:
            api.abort(400, 'Payload vazio.')
        
        if data.get('perfil_id',0) !=0:
            perfil = Perfil.query.filter_by(id=data['perfil_id']).first()
            if not perfil:
                api.abort(404, 'Perfil não encontrado')

        return update_user(usuario, data=data)


@api.route('/<string:campo>/<string:valor>')
@api.response(404, 'Nenhum usuário foi encontrado.')
class Usuario(Resource):    
    @api.marshal_with(_usuariolist, envelope='data')
    @api.doc(security='apikey')
    @admin_token_required
    def get(self, campo, valor):
        """Lista de usuários filtrados por campo/valor"""
        usuarios = get_some_user(campo,valor)
        return usuarios
