from flask_restx import Namespace, fields


class UsuarioDto:
    api = Namespace('usuarios', description='Operações com usuários')
    usuarioinsert = api.model('usuario', {
        'nome': fields.String(required=True, description='nome do usuário'),
        'login': fields.String(required=True, description='login do usuário'),
        'senha': fields.String(required=True, description='senha do usuário'),
    })
    usuariolist = api.model('usuariolist', {
        'id'  : fields.Integer(required=True, description='id do usuário'),
        'nome': fields.String(required=True, description='nome do usuário'),
        'login': fields.String(required=True, description='login do usuário'),
        'senha': fields.String(required=True, description='senha do usuário'),
        'ativo': fields.Boolean(description='status do usuário'),
    })
    usuarioupdate = api.model('usuarioupdate', {
        'nome': fields.String(required=True, description='nome do usuário'),  
        'login': fields.String(required=False, description='login do usuário'),      
        'senha': fields.String(required=True, description='senha do usuário'),
        'ativo': fields.Boolean(required=True,description='inativa/ativa usuário')
    })

class ProdutoDto:
    api = Namespace('produtos', description='Operações com Produtos')
    produto = api.model('produto', {
        'nome': fields.String(required=True, description='nome do usuário'),
        'login': fields.String(required=True, description='login do usuário'),
        'senha': fields.String(required=True, description='senha do usuário'),
    })

class FornecedorDto:
    api = Namespace('fornecedores', description='Endpoint de Fornecedores')
    produto = api.model('fornecedor', {
        'cnpj': fields.String(required=True, description='cpnj do fornecedor'),
        'nome': fields.String(required=True, description='nome fornecedor'),
        'logradouro': fields.String(required=True, description='rua, avenida, estrada, etc'),
        'numero': fields.String(required=True, description='numero do endereço'),
        'complemento': fields.String(required=True, description='complemento do endereço'),
        'bairro': fields.String(required=True, description='bairro'),
        'cidade': fields.String(required=True, description='cidade'),
        'estado': fields.String(required=True, description='estado'),
        'cep': fields.String(required=True, description='cep'),       

    })



class AuthDto:
    api = Namespace('auth', description='Operações de autenticação')
    usuario_auth = api.model('auth_details', {
        'login': fields.String(required=True, description='login do usuário'),
        'senha': fields.String(required=True, description='senha do usuário'),
    })
