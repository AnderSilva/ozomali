from app.main.model.usuario import Usuario
from ..service.blacklist_service import save_token
from ..service.usuario_service import update_password
from typing import Dict, Tuple

class Auth:

    @staticmethod
    def login_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        try:           
            # fetch the usuario data
            usuario = Usuario.query.filter_by(login=data.get('login')).first()
            if usuario and usuario.check_senha(data.get('senha')):
                auth_token = Usuario.encode_auth_token(usuario.id, usuario.nome, usuario.login, usuario.perfil.nome)
                if auth_token:
                    response_object = {
                        'status': 'sucesso',
                        'message': 'Usuário logado com sucesso.',
                        'Authorization': auth_token
                    }
                    return response_object, 200
            else:
                response_object = {
                    'status': 'falha',
                    'message': 'login / senha incorretos.'
                }
                return response_object, 401

        except Exception as e:
            print(e)
            response_object = {
                'status': 'falha',
                'message': 'Tente novamente'
            }
            return response_object, 500

    @staticmethod
    def change_password(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        try:
            novasenha =data.get('novasenha')
            if not novasenha or novasenha.__len__()<4:
                response_object = {
                    'status': 'falha',
                    'message': 'Senha nova deve ser informada com pelo menos 4 digitos.'
                }
                return response_object, 400
            # fetch the usuario data
            usuario = Usuario.query.filter_by(login=data.get('login')).first()
            if usuario and usuario.check_senha(data.get('senha')):
                update_password(usuario, novasenha)
                response_object = {
                    'status': 'sucesso',
                    'message': 'Senha alterada com sucesso.'
                }
                return response_object, 200
            else:
                response_object = {
                    'status': 'falha',
                    'message': 'login / senha incorretos.'
                }
                return response_object, 401

        except Exception as e:
            print(e)
            response_object = {
                'status': 'falha',
                'message': 'Tente novamente'
            }
            return response_object, 500

    @staticmethod
    def reset_password(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        try:
            novasenha =data.get('novasenha')
            if not novasenha or novasenha.__len__()>5:
                response_object = {
                    'status': 'falha',
                    'message': 'Senha nova deve ser informada com pelo menos 4 digitos.'
                }
                return response_object, 400
            # fetch the usuario data
            usuario = Usuario.query.filter_by(login=data.get('login')).first()
            if usuario:
                update_password(usuario, novasenha)
                response_object = {
                    'status': 'sucesso',
                    'message': 'Senha alterada com sucesso.'
                }
                return response_object, 200
            else:
                response_object = {
                    'status': 'falha',
                    'message': 'login / senha incorretos.'
                }
                return response_object, 401

        except Exception as e:
            print(e)
            response_object = {
                'status': 'falha',
                'message': 'Tente novamente'
            }
            return response_object, 500

    @staticmethod
    def logout_user(data: str) -> Tuple[Dict[str, str], int]:
        if data:
            auth_token = data.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Usuario.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                return save_token(token=auth_token)
            else:
                response_object = {
                    'status': 'falha',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'falha',
                'message': 'Forneca um token de autenticação válido.'
            }
            return response_object, 403

    @staticmethod
    def get_logged_in_user(new_request):
        # get the auth token
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            auth_jwt = auth_token.split()[1]
            resp = Usuario.decode_auth_token(auth_jwt)
            if not isinstance(resp, str):
                usuario = Usuario.query.filter_by(id=resp).first()
                response_object = {
                    'status': 'sucesso',
                    'data': {                        
                        'nome': usuario.nome,
                        'uid': usuario.id,
                        'login': usuario.login,
                        'perfil': usuario.perfil.nome                 
                    }
                }
                return response_object, 200
            response_object = {
                'status': 'falha',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'falha',
                'message': 'Forneça um token de autenticação válido.'
            }
            return response_object, 401    
