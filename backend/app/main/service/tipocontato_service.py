import uuid
import datetime

from app.main import db
from app.main.model.tipocontato import TipoContato
from typing import Dict, Tuple


def save_new_contacttype(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    tipocontato = TipoContato.query.filter(
            TipoContato.nome == data['nome']        
    ).first()
    if not tipocontato:
        novo_tipocontato = TipoContato(            
            nome=data['nome'],
        )
        save_changes(novo_tipocontato)
        response_object = {
            'status': 'success',
            'message': 'Tipo Contato registrado com sucesso.',
            'id': novo_tipocontato.id
        }
        return response_object, 201        
    else:
        response_object = {
            'status': 'Falha',
            'message': 'Tipo Contato já existe.',
        }
        return response_object, 409


def get_all_contacttypes(ativo=False):    
    return TipoContato.query.filter_by(ativo=ativo).all()

def get_a_contacttype(id):
    return TipoContato.query.filter_by(id=id).first()

def update_contacttype(tipocontato: TipoContato,data):    
    if data:
        update_changes(tipocontato,data)        
        response_object = {
            'status': 'success',
            'message': 'Tipo contato atualizado com sucesso.',     
        }
        return response_object, 201 #tipo contato para retornar o objeto
    else:
        response_object = {
            'status': 'Falha',
            'message': 'Tipo contato inválido.',
        }
        return response_object, 404


def save_changes(data: TipoContato) -> None:
    db.session.add(data)
    db.session.commit()

def update_changes(tipocontato: TipoContato, data) -> None:
    tipocontato.nome = data.get('nome' , tipocontato.nome)    
    tipocontato.ativo = data.get('ativo', tipocontato.ativo)
    db.session.commit()