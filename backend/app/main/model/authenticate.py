from datetime import datetime

class Authenticate:
    def __init__(self, exp:datetime, iat: datetime, uid: int, name: str, login:str, perfil:str):
        self.exp = exp
        self.iat = iat
        self.uid = uid
        self.name = name
        self.login = login
        self.perfil = perfil

