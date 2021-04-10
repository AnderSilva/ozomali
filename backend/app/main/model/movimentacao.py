from .. import db
import datetime
from typing import Union
from sqlalchemy import func
from .. model.usuario import Usuario
from .. model.produto import Produto    

class Movimentacao(db.Model):
    __tablename__ = "movimentacao"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    local_estoque = db.Column(db.String(50), nullable=False)
    data_movimentacao = db.Column(db.DateTime(timezone=True), onupdate=func.now(), nullable=False)
    tipo_movimentacao = db.Column(db.String(1), nullable=False)
    preco_total = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    usuario_id = db.Column(db.Integer,db.ForeignKey('usuario.id'),nullable=False)
    produto_id = db.Column(db.Integer,db.ForeignKey('produto.id'),nullable=False)
    produto = db.relationship('Produto', backref='produto')
    usuario = db.relationship('Usuario', backref='usuario')

    ativo = db.Column(db.Boolean,default=True)

    def __repr__(self):
        return "<Local Estoque '{}', Produto '{}', Quantidade '{}'>".format(self.local_estoque, self.produto.nome, self.quantidade)
