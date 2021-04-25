from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required, token_required
from app.main.service.auth_helper import Auth
from ..util.dto import AuthDto
from typing import Dict, Tuple

api = AuthDto.api
usuario_auth = AuthDto.usuario_auth
usuario_auth_reset_password = AuthDto.usuario_auth_reset_password
usuario_auth_change_password = AuthDto.usuario_auth_change_password

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

@api.route('/changepassword')
class TrocaSenhaAPI(Resource):
    """
    Change Password
    """
    @api.expect(usuario_auth_change_password, validate=True)
    @api.doc('change a user''s password')
    @api.doc(security='apikey')
    @token_required
    def post(self) -> Tuple[Dict[str, str], int]:
        # get auth token
        post_data = request.json
        return Auth.change_password(data=post_data)

@api.route('/resetpassword')
class ResetSenhaAPI(Resource):
    """
    Reset Password
    """
    @api.expect(usuario_auth_reset_password, validate=True)
    @api.doc('reset a user''s password')
    @api.doc(security='apikey')
    @admin_token_required
    def post(self) -> Tuple[Dict[str, str], int]:
        # get auth token
        post_data = request.json
        return Auth.reset_password(data=post_data)