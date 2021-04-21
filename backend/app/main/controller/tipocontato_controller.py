from flask import request
from flask_restx import Resource

from ..util.dto import TipoContatoDto
from ..service.tipocontato_service import * 
from typing import Dict, Tuple
from app.main.util.decorator import admin_token_required, token_required

api = TipoContatoDto.api
_tipocontatoinsert = TipoContatoDto.tipocontatoinsert
_tipocontatolista = TipoContatoDto.tipocontatolista
_tipocontatoupdate = TipoContatoDto.tipocontatoupdate

@api.route('') #,'/')
class TipoContatoAPI(Resource):
    @api.doc('list_of_registered_users')
    @api.doc(security='apikey')
    @token_required
    @api.marshal_list_with(_tipocontatolista, envelope='data')
    def get(self,ativo=True):
        """Lista todos os tipos contatos"""
        return get_all_contacttypes(ativo)

    @api.expect(_tipocontatoinsert, validate=True)
    @api.response(201, 'Tipo contato criado com sucesso.')
    @api.doc('cria um novo tipo contato')
    @api.doc(security='apikey')
    @token_required
    def post(self) -> Tuple[Dict[str, str], int]:        
        data = request.json
        return save_new_contacttype(data=data)


@api.route('/<int:id>')
@api.param('id', 'Identificador do tipo contato')
@api.response(404, 'Tipo contato não encontrado.')
class Contato(Resource):
    @api.doc('get a tipo contato')
    @api.marshal_with(_tipocontatolista)
    @api.doc(security='apikey')
    @token_required
    def get(self, id):
        """Obtem informações de um tipo contato com base no seu id"""
        tipocontato = get_a_contacttype(id)
        if not tipocontato:
            api.abort(404)
        else:
            return tipocontato


    @api.doc('Atualiza um tipo contato')
    @api.expect(_tipocontatoupdate) #, validate=True)
    @api.response(201, 'Tipo contato atualizado com sucesso.')
    #@api.marshal_with(_perfillist) para retornar o objeto
    @api.doc(security='apikey')
    @token_required
    def patch(self,id): # -> Tuple[Dict[str, str], int]:        
        """Atualiza um tipo contato  Obs: para inativar, coloque 'ativo': false """
        
        tipocontato = get_a_contacttype(id)
        if not tipocontato:
            api.abort(404)
        else:
            data = request.json        
            return update_contacttype(tipocontato,data=data)

@api.route('/inativos')
class TipoContatoListaInativo(Resource):
    @api.doc('lista tipo contato inativos')
    @api.doc(security='apikey')
    @token_required
    @api.marshal_list_with(_tipocontatolista, envelope='data')
    def get(self,ativo=False):
        """Lista todos tipos contatos inativos"""
        return get_all_contacttype(ativo)

            