import uuid
import datetime

from app.main import db
from app.main.model.perfil import Perfil
from typing import Dict, Tuple


def save_new_profile(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    perfil = Perfil.query.filter(
            Perfil.nome == data['nome']        
    ).first()
    if not perfil:
        novo_perfil = Perfil(            
            nome=data['nome'],
        )
        save_changes(novo_perfil)
        response_object = {
            'status': 'Sucesso',
            'message': 'Perfil registrado com sucesso.',
            'id': novo_perfil.id,
        }
        return response_object, 201        
    else:
        response_object = {
            'status': 'Falha',
            'message': 'Perfil já existe.',
        }
        return response_object, 409


def update_profile(perfil: Perfil,data):    
    update_changes(perfil,data)        
    return perfil

def get_all_profiles(ativo=False):    
    return Perfil.query.filter_by(ativo=ativo).all()


def get_a_profile(id):
    return Perfil.query.filter_by(id=id).first()

def save_changes(data: Perfil) -> None:
    db.session.add(data)
    db.session.commit()

def update_changes(perfil: Perfil, data) -> None:
    perfil.nome = data.get('nome' , perfil.nome)    
    perfil.ativo = data.get('ativo', perfil.ativo)
    db.session.commit()