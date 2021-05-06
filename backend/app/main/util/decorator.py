from functools import wraps

from flask import request

from app.main.service.auth_helper import Auth
from typing import Callable


def token_required(f) -> Callable:
    @wraps(f)
    def decorated(self, *args, **kwargs):
        data, status = Auth.get_logged_in_user(request)        
        token = data.get('data')
        self.uid = token.get('uid')
        if not token:
            return data, status

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
                'status': 'falha',
                'message': 'requirido token admin'
            }
            return response_object, 401

        return f(*args, **kwargs)

    return decorated
