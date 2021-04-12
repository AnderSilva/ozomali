import uuid
import datetime

from app.main import db
from app.main.model.fornecedor import Fornecedor
from app.main.model import unaccent
from typing import Dict, Tuple


def save_new_vendor(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    fornecedor = Fornecedor.query.filter(
        db.or_(
             Fornecedor.cnpj == data['cnpj'],
        )
    ).first()
    if not fornecedor:
        novo_fornecedor = Fornecedor(            
            cnpj=data['cnpj'],
            nome=data['nome'],
            logradouro=data['logradouro'],
            numero=data['numero'],
            complemento=data.get('complemento', ''),
            bairro=data['bairro'],
            cidade=data['cidade'],
            estado=data['estado'],
            cep=data['cep'],
            ativo=True,
        )
        save_changes(novo_fornecedor)
        response_object = {
            'status': 'success',
            'message': 'Fornecedor registrado com sucesso.',
            'id': novo_fornecedor.id
        }
        return response_object, 201
        # return generate_token(new_user)
    else:
        response_object = {
            'status': 'Falha',
            'message': 'CNPJ já existe.',
        }
        return response_object, 409

def update_vendor(fornecedor: Fornecedor,data):    
    update_changes(fornecedor,data)        
    return fornecedor

def get_all_vendors(ativo=False):    
    return Fornecedor.query.filter_by(ativo=ativo).all()

def get_a_vendor(id):
    return Fornecedor.query.filter_by(id=id).first()

def get_some_vendor(nome):
    item = '%{}%'.format(nome)
    filter1 = unaccent(Fornecedor.nome).ilike(item)
    filter2 = Fornecedor.nome.ilike(item)

    return Fornecedor.query \
    .filter(
        db.or_(filter1, filter2)
    ).all()


def save_changes(data: Fornecedor) -> None:
    db.session.add(data)
    db.session.commit()

def update_changes(fornecedor: Fornecedor, data) -> None:
    fornecedor.cnpj = data.get('cnpj' , fornecedor.cnpj)
    fornecedor.nome = data.get('nome' , fornecedor.nome)
    fornecedor.logradouro = data.get('logradouro' , fornecedor.logradouro)
    fornecedor.numero = data.get('numero' , fornecedor.numero)
    fornecedor.complemento = data.get('complemento' , fornecedor.complemento)
    fornecedor.bairro = data.get('bairro' , fornecedor.bairro)
    fornecedor.cidade = data.get('cidade' , fornecedor.cidade)
    fornecedor.estado = data.get('estado' , fornecedor.estado)
    fornecedor.cep = data.get('cep' , fornecedor.cep)    
    fornecedor.ativo = data.get('ativo', fornecedor.ativo)
    db.session.commit()
