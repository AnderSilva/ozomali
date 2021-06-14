from functools import wraps

from flask import request

from app.main.service.auth_helper import Auth
from typing import Callable
from app.main.model.authenticate import Authenticate


def token_required(f) -> Callable:
    @wraps(f)
    def decorated(self, *args, **kwargs):
        data, status = Auth.get_logged_in_user(request)        
        token = data.get('data')        
        if not token:
            return data, status
        get_authenticate(self, token)

        return f(self, *args, **kwargs)

    return decorated


def admin_token_required(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        admin = token.get('perfil')
        if not admin or admin != 'admin':
            response_object = {
                'status': 'Falha',
                'message': 'Acesso não autorizado'
            }
            return response_object, 401

        return f(*args, **kwargs)

    return decorated

def get_authenticate(self, token):
    self.authenticate = Authenticate(token.get('exp',''), token.get('iat',''), token.get('uid',''), token.get('name',''), token.get('login',''), token.get('perfil',''))
