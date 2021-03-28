from flask_restx import Api
from flask import Blueprint

from .main.controller.usuario_controller import api as user_ns
from .main.controller.produto_controller import api as product_ns

from .main.controller.auth_controller import api as auth_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='OZOMALI API RESTFULL', # WITH JWT AUTH',
          version='2.0',
          description='By Ozomali development team'
          )

api.add_namespace(user_ns, path='/users')
api.add_namespace(product_ns, path='/products')


# TODO API DE FORNECEDOR
# api.add_namespace(vendor_ns, path='/vendors')

# TODO AUTH JWT
# api.add_namespace(auth_ns)