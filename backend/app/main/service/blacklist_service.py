# from app.main import db

# from app.main.model.blacklist import BlacklistToken
# from typing import Dict, Tuple


# def save_token(token: str) -> Tuple[Dict[str, str], int]:
#     blacklist_token = BlacklistToken(token=token)
#     try:
#         # insert the token
#         db.session.add(blacklist_token)
#         db.session.commit()
#         response_object = {
#             'status': 'successo',
#             'message': 'Usuário deslogado com sucesso.'
#         }
#         return response_object, 200
#     except Exception as e:
#         response_object = {
#             'status': 'falha',
#             'message': e
#         }
#         return response_object, 200
