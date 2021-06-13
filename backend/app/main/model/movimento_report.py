from .. import db
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property

class MovimentoReport(db.Model):
    __tablename__ = "vw_movimentacao_report"

    id = db.Column(db.Integer, primary_key=True)
    data_filtro = db.Column(db.String(10))
    visao_filtro = db.Column(db.String(10))
    periodo = db.Column(db.String(10))
    vendas = db.Column(db.Float)
    compras = db.Column(db.Float)
    lucro_prejuizo = db.Column(db.Float)
    ticket_medio = db.Column(db.Float)

    def __repr__(self):
        return "<Movimento '{}'>".format(self.visao_filtro)

    def __init__(self, data_filtro:str, visao_filtro: str, periodo: str, vendas: float, compras:float, lucro_prejuizo:float, ticket_medio:float):
        self.data_filtro = data_filtro
        self.visao_filtro = visao_filtro
        self.periodo = periodo
        self.vendas = round(vendas, ndigits=2)
        self.compras = round(compras, ndigits=2)
        self.lucro_prejuizo = round(lucro_prejuizo, ndigits=2)
        self.ticket_medio = round(ticket_medio, ndigits=2)

#CREATE OR REPLACE VIEW vw_movimentacao_report AS
# select row_number() over(ORDER BY data_filtro) as id, data_filtro, visao_filtro, periodo, round(cast(vendas as numeric),2) vendas, round(cast(compras as numeric),2) compras, round(cast(lucro_prejuizo as numeric),2) lucro_prejuizo,round(cast(ticket_medio as numeric),2) ticket_medio from ( 
# select TO_CHAR(m.data_movimentacao,'Mon/yy') as periodo, TO_CHAR(m.data_movimentacao,'yyyyMM01') as data_filtro,
# 'Mensal' as visao_filtro, 
# sum(case when m.tipo_movimentacao = 'S' then m.preco_total else 0 end) as vendas,
# sum(case when m.tipo_movimentacao = 'E' then m.preco_total else 0 end) as compras,
# sum((case when m.tipo_movimentacao = 'S' then 1 else -1 end) * m.preco_total) as lucro_prejuizo,
# (case when sum(case when m.tipo_movimentacao = 'S' then m.quantidade else 0 end) = 0 then 0 else 
# (sum(case when m.tipo_movimentacao = 'S' then m.preco_total else 0 end)
# /sum(case when m.tipo_movimentacao = 'S' then m.quantidade else 0 end)) 
# end) as ticket_medio
# from movimentacao m
# where m.ativo = true
# group by TO_CHAR(m.data_movimentacao,'Mon/yy'),TO_CHAR(m.data_movimentacao,'yyyyMM01')
# union 
# select TO_CHAR(m.data_movimentacao,'dd/MM/yyyy') as periodo, TO_CHAR(m.data_movimentacao,'yyyyMMdd') as data_filtro,
# 'Diario' as visao_filtro, 
# sum(case when m.tipo_movimentacao = 'S' then m.preco_total else 0 end) as vendas,
# sum(case when m.tipo_movimentacao = 'E' then m.preco_total else 0 end) as compras,
# sum((case when m.tipo_movimentacao = 'S' then 1 else -1 end) * m.preco_total) as lucro_prejuizo,
# (case when sum(case when m.tipo_movimentacao = 'S' then m.quantidade else 0 end) = 0 then 0 else 
# (sum(case when m.tipo_movimentacao = 'S' then m.preco_total else 0 end)
# /sum(case when m.tipo_movimentacao = 'S' then m.quantidade else 0 end)) 
# end) as ticket_medio
# from movimentacao m
# where m.ativo = true
# group by TO_CHAR(m.data_movimentacao,'dd/MM/yyyy'),TO_CHAR(m.data_movimentacao,'yyyyMMdd')
# union 
# select TO_CHAR(date_trunc('week', m.data_movimentacao),'dd/Mon') as periodo, TO_CHAR(date_trunc('week', m.data_movimentacao),'yyyyMMdd') as data_filtro,
# 'Semanal' as visao_filtro, 
# sum(case when m.tipo_movimentacao = 'S' then m.preco_total else 0 end) as vendas,
# sum(case when m.tipo_movimentacao = 'E' then m.preco_total else 0 end) as compras,
# sum((case when m.tipo_movimentacao = 'S' then 1 else -1 end) * m.preco_total) as lucro_prejuizo,
# (case when sum(case when m.tipo_movimentacao = 'S' then m.quantidade else 0 end) = 0 then 0 else 
# (sum(case when m.tipo_movimentacao = 'S' then m.preco_total else 0 end)
# /sum(case when m.tipo_movimentacao = 'S' then m.quantidade else 0 end)) 
# end) as ticket_medio
# from movimentacao m
# where m.ativo = true
# group by TO_CHAR(date_trunc('week', m.data_movimentacao),'dd/Mon'),TO_CHAR(date_trunc('week', m.data_movimentacao),'yyyyMMdd')
# ) as t order by t.data_filtro
