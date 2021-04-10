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

# from .main.controller.auth_controller import api as auth_ns

# blueprint = Blueprint('api', __name__)
blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

api = Api(blueprint,
          title='OZOMALI API RESTFULL', # WITH JWT AUTH',
          version='2.0',
          description='By Ozomali development team'
          )

api.add_namespace(usuario_ns, path='/usuarios')
api.add_namespace(perfil_ns, path='/perfis')
api.add_namespace(tipocontato_ns, path='/tipocontatos')
api.add_namespace(fornecedor_ns, path='/fornecedores')
api.add_namespace(contato_ns, path='/contatos')
api.add_namespace(preco_ns, path='/precos')
api.add_namespace(movimentacao_ns, path='/movimentacoes')

# TODO PRECOS - validar e testar
# api.add_namespace(preco_ns, path='/precos')


# TODO FORNECEDOR - validar e testar
# api.add_namespace(fornecedor_ns, path='/fornecedores')

# TODO AUTH JWT
# api.add_namespace(auth_ns)

api.add_namespace(produto_ns, path='/produtos')