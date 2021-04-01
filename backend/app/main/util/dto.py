from flask_restx import Namespace, fields
from .. model.perfil import Perfil

class PerfilDto:
    api = Namespace('perfil', description='Operações com Perfis de Usuario')
    perfil = api.model('perfil', {
        'nome': fields.String(required=True, description='nome do perfil'),
        'uri' : fields.Url('api.perfil_perfil', readonly=True),
    })

class UsuarioDto:
    api = Namespace('usuarios', description='Operações com usuários')

    perfil = api.model('perfil', {
        'id': fields.String( description='nome do perfil'),
        'nome': fields.String( description='nome do perfil'),        
        'uri' : fields.Url('api.perfil_perfil', readonly=True),
    })
    usuarioinsert = api.model('usuario', {
        'login': fields.String(required=True),
        'senha': fields.String(required=True),
    })
    usuariolist = api.model('usuariolist', {
        'id'  : fields.Integer(readonly=True),        
        'login': fields.String(required=True),
        'senha': fields.String(attribute='senhaHash'),
        'ativo': fields.Boolean(),
        'uri' : fields.Url('api.usuarios_usuario'),
        'perfil': fields.Nested(perfil,as_list=False)
    })
    usuarioupdate = api.clone('usuarioupdate', usuarioinsert, {
        'ativo': fields.Boolean(required=True,description='inativa/ativa usuário')
    })

class ProdutoDto:
    api = Namespace('produtos', description='Operações com Produtos')
    produto = api.model('produto', {
        'nome': fields.String(required=True, description='nome do usuário'),
        'uri' : fields.Url('api.produtos_produto'),
    })

class PrecoDto:
    api = Namespace('precos', description='Operações com Precos')
    preco = api.model('preco', {
        'PrecoVenda': fields.String(required=True, description='Preco de venda'),
        'uri' : fields.Url('api.precos_preco'),
    })


class FornecedorDto:
    api = Namespace('fornecedores', description='Endpoint de Fornecedores')
    fornecedor = api.model('fornecedor', {
        'cnpj': fields.String(required=True, description='cpnj do fornecedor'),
        'nome': fields.String(required=True, description='nome fornecedor'),
        'logradouro': fields.String(required=True, description='rua, avenida, estrada, etc'),
        'numero': fields.String(required=True, description='numero do endereço'),
        'complemento': fields.String(required=True, description='complemento do endereço'),
        'bairro': fields.String(required=True, description='bairro'),
        'cidade': fields.String(required=True, description='cidade'),
        'estado': fields.String(required=True, description='estado'),
        'cep': fields.String(required=True, description='cep'),
        'uri' : fields.Url('api.fornecedores_fornecedor'),

    })



class AuthDto:
    api = Namespace('auth', description='Operações de autenticação')
    usuario_auth = api.model('auth_details', {
        'login': fields.String(required=True, description='login do usuário'),
        'senha': fields.String(required=True, description='senha do usuário'),
    })
