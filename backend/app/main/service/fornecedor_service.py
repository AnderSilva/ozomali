import uuid
import datetime
import unidecode

from app.main import db
from app.main.model.fornecedor import Fornecedor
from app.main.model import unaccent
from typing import Dict, Tuple
from sqlalchemy.sql import text

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
            'status': 'Sucesso',
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
        return response_object, 400

def update_vendor(fornecedor: Fornecedor,data)-> Tuple[Dict[str, str], int]:
    update_changes(fornecedor,data)
    response_object = {
            'status': 'Sucesso',
            'message': 'Fornecedor atualizado com sucesso.',
            'id' : fornecedor.id,
            'cnpj':fornecedor.cnpj,
            'nome' : fornecedor.nome,
            'logradouro' : fornecedor.logradouro,
            'numero' : fornecedor.numero,
            'complemento' : fornecedor.complemento,
            'bairro' : fornecedor.bairro,
            'cidade' : fornecedor.cidade,
            'estado' : fornecedor.estado,
            'cep' : fornecedor.cep,
            'ativo' : fornecedor.ativo,
        }
    return response_object, 200    

def get_all_vendors():    
    return Fornecedor.query.all()

def get_search_vendors(data):
    filters = ''
    if data.get('nome',''):
        filters += "LOWER(unaccent(nome)) like '%" + unidecode.unidecode(data.get('nome','')).lower() + "%'"

    if data.get('id',0) != 0:
        if filters:
            filters += " AND "
        filters += "id = " + str(data.get('id',0))

    if data.get('cnpj',''):
        if filters:
            filters += " AND "
        filters += "cnpj like '%" + data.get('cnpj','') + "%'"
    
    if data.get('logradouro',''):
        if filters:
            filters += " AND "
        filters += "LOWER(unaccent(logradouro)) like '%" + unidecode.unidecode(data.get('logradouro','')).lower() + "%'"
    
    if data.get('numero',''):
        if filters:
            filters += " AND "
        filters += "LOWER(unaccent(numero)) like '%" + unidecode.unidecode(data.get('numero','')).lower() + "%'"

    if data.get('complemento',''):
        if filters:
            filters += " AND "
        filters += "LOWER(unaccent(complemento)) like '%" + unidecode.unidecode(data.get('complemento','')).lower() + "%'"
    
    if data.get('bairro',''):
        if filters:
            filters += " AND "
        filters += "LOWER(unaccent(bairro)) like '%" + unidecode.unidecode(data.get('bairro','')).lower() + "%'"

    if data.get('cidade',''):
        if filters:
            filters += " AND "
        filters += "LOWER(unaccent(cidade)) like '%" + unidecode.unidecode(data.get('cidade','')).lower() + "%'"

    if data.get('estado',''):
        if filters:
            filters += " AND "
        filters += "LOWER(unaccent(estado)) like '%" + unidecode.unidecode(data.get('estado','')).lower() + "%'"

    if data.get('cep',''):
        if filters:
            filters += " AND "
        filters += "LOWER(unaccent(cep)) like '%" + unidecode.unidecode(data.get('cep','')).lower() + "%'"

    if data.get('ativo','') == False or data.get('ativo','')== True:
        if filters:
            filters += " AND "
        filters += "ativo =" 
        filters += "'true'" if data.get('ativo','')== True else "'false'"    

    return Fornecedor.query.filter(text(filters)).all()

def get_a_vendor(tipo, id):
    item = '%{}%'.format(id)

    if tipo=='id':
        return Fornecedor.query.filter_by(id=id).first()

    if tipo=='nome':
        filter1 = unaccent(Fornecedor.nome).ilike(item)
        filter2 = Fornecedor.nome.ilike(item)
        return Fornecedor.query.filter(
            db.or_(filter1, filter2)
        ).all()

    if tipo=='cnpj':
        return Fornecedor.query.filter_by(cnpj=id).first()

    if tipo=='bairro':
        return Fornecedor.query.filter(
            unaccent(Fornecedor.bairro).ilike(item)
        ).all()

    if tipo=='cidade':        
        return Fornecedor.query.filter(
            unaccent(Fornecedor.cidade).ilike(item)
        ).all()

    if tipo=='estado':
        return Fornecedor.query.filter(
            unaccent(Fornecedor.estado).ilike(item)
        ).all()

    if tipo=='cep':
        return Fornecedor.query.filter_by(cep=id).all()
    
    if tipo=='ativo':
        return Fornecedor.query.filter_by(ativo=id).all()
    
    
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
