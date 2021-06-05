import uuid
import datetime

from app.main import db
from app.main.model.contato import Contato
from app.main.model.tipocontato import TipoContato
from app.main.model.fornecedor import Fornecedor
from typing import Dict, Tuple


def save_new_contact(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    
    tipocontato = TipoContato.query.filter(
        TipoContato.id == data['tipocontato_id'],
        TipoContato.ativo == True
    ).first()
    if not tipocontato:
        response_object = {
            'status': 'Falha',
            'message': 'Tipo de contato inválido.',
        }
        return response_object, 404
    
    fornecedor = Fornecedor.query.filter(
        Fornecedor.id == data['fornecedor_id']
    ).first()
    if not fornecedor:
        response_object = {
            'status': 'Falha',
            'message': 'Fornecedor inválido',
        }
        return response_object, 404

    contato = Contato.query.filter(
        db.and_(
             Contato.tipocontato_id == data['tipocontato_id'],
             Contato.valor == data['valor'],
             Contato.fornecedor_id == data['fornecedor_id'],
        )
    ).first()
    if not contato:
        novo_contato = Contato(            
            valor=data['valor'],
            tipocontato_id=data['tipocontato_id'],
            fornecedor_id=data['fornecedor_id'],
            ativo=True,
        )
        save_changes(novo_contato)
        response_object = {
            'status': 'Sucesso',
            'message': 'Contato registrado com sucesso.',
            'id': novo_contato.id
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'Falha',
            'message': 'Contato já existe.',
        }
        return response_object, 409

def get_all_contacts(ativo=False):    
    return Contato.query.filter_by(ativo=ativo).all()

def get_a_contact(id):
    return Contato.query.filter_by(id=id).first()

def update_contact(contato: Contato,data):    
    if data:
        # validando se esse tipo contato existe
        if data.get('tipocontato_id',-1) != -1:
            tipocontato = TipoContato.query.filter(
                TipoContato.id == data['tipocontato_id'],
                TipoContato.status == True
            ).first()
            if not tipocontato:
                response_object = {
                    'status': 'Falha',
                    'message': 'Tipo de contato inválido.',
                }
                return response_object, 404

        update_changes(contato,data)        
        response_object = {
            'status': 'Sucesso',
            'message': 'Contato atualizado com sucesso.'     
        }
        return response_object, 201 #tipo contato para retornar o objeto
    else:
        response_object = {
            'status': 'Falha',
            'message': 'Contato inválido.',
        }
        return response_object, 404


def save_changes(data: Contato) -> None:
    db.session.add(data)
    db.session.commit()

def update_changes(contato: Contato, data) -> None:
    contato.valor = data.get('valor' , contato.valor)    
    contato.ativo = data.get('ativo', contato.ativo)
    contato.tipocontato_id = data.get('tipocontato_id', contato.tipocontato_id)
    db.session.commit()
