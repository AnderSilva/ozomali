from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('user', description='Operações relacionadas a usuários')
    user = api.model('user', {
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
