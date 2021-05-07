
from .. import db
import datetime
from ..config import key
from sqlalchemy.ext.hybrid import hybrid_property
from typing import Union
from .. model.fornecedor import Fornecedor

class Produto(db.Model):    
    __tablename__ = "produto"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    nome = db.Column(db.String(100), unique=True, nullable=False)
    codigo_barra = db.Column(db.String(50), unique=True, nullable=True)
    fornecedor_id = db.Column(db.Integer,db.ForeignKey('fornecedor.id'))
    precos = db.relationship("Preco")
    movimentacoes = db.relationship("Movimentacao")
    @hybrid_property
    def preco_venda(self):        
        for p in self.precos:
            if p.ativo:
                return p.preco_venda
        return 0
    @hybrid_property
    def saldo(self):        
        _saldo = 0
        for p in self.movimentacoes:
            if p.tipo_movimentacao == "S":
                _saldo -= p.quantidade
            else:
                _saldo += p.quantidade
        return _saldo

    ativo = db.Column(db.Boolean,default=True, nullable=False)                

    def __repr__(self):    
        return f'Produto(id:"{self.id}",nome:"{self.nome}",codigo_barra:"{self.codigo_barra}",fornecedor_id:"{self.fornecedor_id},ativo:"{self.ativo}")'    