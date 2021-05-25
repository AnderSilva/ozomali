from re import DOTALL
from typing import Dict, Tuple

from sqlalchemy.sql.expression import false, true
from app.main.model.movimento_report import MovimentoReport
from sqlalchemy.sql import text
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse

def get_movi_order(employee):
    return employee.data_filtro

def movimento_validacao(data) -> Tuple[Dict[str,str], int]:
    if not data.get('periodo','') in ['Mensal', 'Semanal', 'Diario']:
        response_object = {
                'status': 'Falha',
                'message': 'Periodo invalido [%s], os periodos validos são Mensal, Semanal e Diario.'.format(data.get('periodo','')),
            }
        return response_object, 400
    if not is_date(data.get('data_inicio','')):
        response_object = {
                'status': 'Falha',
                'message': 'Data inicio é invalida [%s] o formato é yyyymmdd'.format(data.get('data_inicio','')),
            }
        return response_object, 400
    if not is_date(data.get('data_final','')):
        response_object = {
                'status': 'Falha',
                'message': 'Data final é invalida [%s] o formato é yyyymmdd'.format(data.get('data_final','')),
            }
        return response_object, 400
    if data.get('data_final','')<data.get('data_inicio',''):
        response_object = {
                'status': 'Falha',
                'message': 'Data final deve ser maior que data inicial.',
            }
        return response_object, 400

    response_object = {
                'status': 'Sucesso',
                'message': '',
            }
    return  response_object,200
    
def is_date(data):    
    try: 
        #dt = data[0,4] + '-' + data[4,6] + '-' + data[6,8]
        parse(data)
        return True
    except ValueError:
        return False

def movimentacao_report_by_periodo(data):    
    filters = ''
    filters += "visao_filtro = '" + data.get('periodo','') + "'"
    if data.get('data_inicio',''):
        filters += " AND "
        filters += "data_filtro >= '" + data.get('data_inicio','') + "'"
    if data.get('data_final',''):
        filters += " AND "
        filters += "data_filtro <= '" + data.get('data_final','') + "'"
    data_report = MovimentoReport.query.filter(text(filters)).all()
    data_report = addPeriodoVazios(data_report, data)    
    data_report.sort(key=get_movi_order)
    return data_report

def addPeriodoVazios(lista, data):
    dataini = data.get('data_inicio','')
    datafin = data.get('data_final','')
    periodo = data.get('periodo','')    
    if periodo == 'Mensal':
        while (dataini <= datafin):
            findflag = false
            for m in lista:
                if m.data_filtro == dataini:
                    findflag = true 
                    break
            if findflag == false:
                dtiniDate = datetime.strptime(dataini[0:4] + '-' + dataini[4:6] + '-01', '%Y-%m-%d')
                lista.append(MovimentoReport(dataini, 'Mensal', dtiniDate.strftime('%b/%y'), 0, 0,0,0))
            dataini = GetDatePlus(dataini, 1,0,0)
    if periodo == 'Semanal':
        dataini = GetIniSemanal(dataini)
        while (dataini <= datafin):
            findflag = false
            for m in lista:
                if m.data_filtro == dataini:
                    findflag = true 
                    break
            if findflag == false:
                dtiniDate = datetime.strptime(dataini[0:4] + '-' + dataini[4:6] + '-' + dataini[6:8], '%Y-%m-%d')
                lista.append(MovimentoReport(dataini, 'Diario', dtiniDate.strftime('%d/%b'), 0, 0,0,0))
            dataini = GetDatePlus(dataini, 0,1,0)
    if periodo == 'Diario':
        while (dataini <= datafin):
            findflag = false
            for m in lista:
                if m.data_filtro == dataini:
                    findflag = true 
                    break
            if findflag == false:
                dtiniDate = datetime.strptime(dataini[0:4] + '-' + dataini[4:6] + '-' + dataini[6:8], '%Y-%m-%d')
                lista.append(MovimentoReport(dataini, 'Diario', dtiniDate.strftime('%d/%b'), 0, 0,0,0))
            dataini = GetDatePlus(dataini, 0,0,1)
    return lista

def GetDatePlus(dateStr, months, weeks, days) -> str:
    dtini = datetime.strptime(dateStr[0:4] + '-' + dateStr[4:6] + '-' + dateStr[6:8], '%Y-%m-%d')
    dtini = dtini + relativedelta(months=months, weeks=weeks,days=days)    
    dtindex =  dtini.strftime('%Y%m%d')
    return dtindex

def GetIniSemanal(dateStr) ->str:
    dtini = datetime.strptime(dateStr[0:4] + '-' + dateStr[4:6] + '-' + dateStr[6:8], '%Y-%m-%d')    
    while(dtini.weekday() != 0):
        dtini = dtini + relativedelta(days=1)
    return dtini.strftime('%Y%m%d')