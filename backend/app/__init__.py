from flask_restx import Api
from flask import Blueprint

from .main.controller.usuario_controller import api as usuario_ns
from .main.controller.perfil_controller import api as perfil_ns
from .main.controller.produto_controller import api as produto_ns
from .main.controller.preco_controller import api as preco_ns
from .main.controller.fornecedor_controller import api as fornecedor_ns
from .main.controller.tipocontato_controller import api as tipocontato_ns
from .main.controller.contato_controller import api as contato_ns
from .main.controller.movimentacao_controller import api as movimentacao_ns
from .main.controller.auth_controller import api as auth_ns
from pathlib import Path
from datetime import datetime

# from .main.controller.auth_controller import api as auth_ns

# blueprint = Blueprint('api', __name__)
blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

authorizations = {
    'apikey' : {
        'type' : 'apiKey',
        'in' : 'header',
        'name' : 'Authorization'
    },
}

diretorio = Path('.')
dt_release = datetime.fromtimestamp(diretorio.stat().st_mtime)

api = Api(blueprint,
          title='OZOMALI API RESTFULL', # WITH JWT AUTH',
          version='2.0',
          description='By Ozomali development team | last update: ' + dt_release.strftime("%d/%m/%Y, %H:%M:%S"),
          security = 'apiKey',
          authorizations=authorizations
          )
 
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(usuario_ns, path='/usuarios')
api.add_namespace(perfil_ns, path='/perfis')
api.add_namespace(fornecedor_ns, path='/fornecedores')
api.add_namespace(contato_ns, path='/contatos')
api.add_namespace(tipocontato_ns, path='/tipocontatos')
api.add_namespace(produto_ns, path='/produtos')
api.add_namespace(movimentacao_ns, path='/movimentacoes')
api.add_namespace(preco_ns, path='/precos')



# TODO AUTH JWT
# api.add_namespace(auth_ns)
