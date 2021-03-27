from app.main.model.user import User
from ..service.blacklist_service import save_token
from typing import Dict, Tuple


class Auth:

    @staticmethod
    def login_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        try:
            # fetch the user data
            user = User.query.filter_by(login=data.get('login')).first()
            if user and user.check_password(data.get('senha')):
                auth_token = User.encode_auth_token(user.id)
                if auth_token:
                    response_object = {
                        'status': 'sucesso',
                        'message': 'Usuário logado com sucesso.',
                        'Authorization': auth_token.decode()
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
            resp = User.decode_auth_token(auth_token)
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
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                response_object = {
                    'status': 'successo',
                    'data': {                        
                        'nome': user.nome,
                        'login': user.login
                        
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
