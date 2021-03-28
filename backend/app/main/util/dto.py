from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('user', description='Endpoint de usuários')
    userinsert = api.model('user', {
        'nome': fields.String(required=True, description='nome do usuário'),
        'login': fields.String(required=True, description='login do usuário'),
        'senha': fields.String(required=True, description='senha do usuário'),
    })
    userlist = api.model('userlist', {
        'id'  : fields.Integer(required=True, description='id do usuário'),
        'nome': fields.String(required=True, description='nome do usuário'),
        'login': fields.String(required=True, description='login do usuário'),
        'senha': fields.String(required=True, description='senha do usuário'),
        'ativo': fields.Boolean(description='status do usuário'),
    })
    userupdate = api.model('userupdate', {
        'nome': fields.String(required=True, description='nome do usuário'),  
        'login': fields.String(required=False, description='login do usuário'),      
        'senha': fields.String(required=True, description='senha do usuário'),
        'ativo': fields.Boolean(required=True,description='inativa/ativa usuário')
    })

class ProdutoDto:
    api = Namespace('product', description='Endpoint de Produtos')
    produto = api.model('produto', {
        'nome': fields.String(required=True, description='nome do usuário'),
        'login': fields.String(required=True, description='login do usuário'),
        'senha': fields.String(required=True, description='senha do usuário'),
    })



class AuthDto:
    api = Namespace('auth', description='Operações de autenticação')
    user_auth = api.model('auth_details', {
        'login': fields.String(required=True, description='login do usuário'),
        'senha': fields.String(required=True, description='senha do usuário'),
    })
