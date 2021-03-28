from flask_restx import Api
from flask import Blueprint

from .main.controller.usuario_controller import api as usuario_ns
from .main.controller.produto_controller import api as produto_ns
# from .main.controller.fornecedor_controller import api as fornecedor_ns

from .main.controller.auth_controller import api as auth_ns

# blueprint = Blueprint('api', __name__)
blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

api = Api(blueprint,
          title='OZOMALI API RESTFULL', # WITH JWT AUTH',
          version='2.0',
          description='By Ozomali development team'
          )

api.add_namespace(usuario_ns, path='/usuarios')

# TODO PRODUTOS
# api.add_namespace(produto_ns, path='/produtos')


# TODO FORNECEDOR
# api.add_namespace(fornecedor_ns, path='/fornecedores')

# TODO AUTH JWT
# api.add_namespace(auth_ns)