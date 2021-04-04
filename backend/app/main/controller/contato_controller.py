from flask import request
from flask_restx import Resource

# from app.main.util.decorator import admin_token_required
from ..util.dto import ContatoDto
from ..service.contato_service import * 
from typing import Dict, Tuple

api = ContatoDto.api
_contatoinsert = ContatoDto.contatoinsert
_contatolista = ContatoDto.contatolista
_contatoupdate = ContatoDto.contatoupdate

@api.route('') #,'/')
class ContatoApi(Resource):
    @api.doc('lista contatos ativos')
    # @admin_token_required
    @api.marshal_list_with(_contatolista, envelope='data')
    def get(self,ativo=True):
        """Lista todos os contatos"""
        return get_all_contacts(ativo)

    @api.expect(_contatoinsert, validate=True)
    @api.response(201, 'Contato criado com sucesso.')
    @api.doc('cria um novo contato')
    def post(self) -> Tuple[Dict[str, str], int]:        
        data = request.json
        return save_new_contact(data=data)

@api.route('/<int:id>')
@api.param('id', 'Identificador do contato')
@api.response(404, 'Contato não encontrado.')
class Contato(Resource):
    @api.doc('obter contato')
    @api.marshal_with(_contatolista)
    def get(self, id):
        """Obtem informações de um contato com base no seu id"""
        contato = get_a_contact(id)
        if not contato:
            api.abort(404)
        else:
            return contato

    @api.doc('Atualiza um contato')
    @api.expect(_contatoupdate) #, validate=True)
    @api.response(201, 'Contato atualizado com sucesso.')
    #@api.marshal_with(_perfillist) para retornar o objeto
    def patch(self,id): # -> Tuple[Dict[str, str], int]:        
        """Atualiza um contato  Obs: para inativar, coloque 'ativo': false """
        
        contato = get_a_contact(id)
        if not contato:
            api.abort(404)
        else:
            data = request.json        
            return update_contact(contato,data=data)

@api.route('/inativos')
class ContatoListaInativo(Resource):
    @api.doc('lista contato inativos')
    # @admin_token_required
    @api.marshal_list_with(_contatolista, envelope='data')
    def get(self,ativo=False):
        """Lista todos contatos inativos"""
        return get_all_contacts(ativo)




