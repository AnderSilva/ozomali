from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required, token_required
from app.main.service.auth_helper import Auth
from ..util.dto import AuthDto
from typing import Dict, Tuple

api = AuthDto.api
usuario_auth = AuthDto.usuario_auth


@api.route('/login')
class UsuarioLogin(Resource):
    """
        Usuario Login Resource
    """
    @api.doc('login do usuario')
    @api.expect(usuario_auth, validate=True)
    def post(self) -> Tuple[Dict[str, str], int]:
        # get the post data
        post_data = request.json
        return Auth.login_user(data=post_data)


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @api.doc('logout a user')
    @api.doc(security='apikey')
    @token_required
    def post(self) -> Tuple[Dict[str, str], int]:
        # get auth token
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)
