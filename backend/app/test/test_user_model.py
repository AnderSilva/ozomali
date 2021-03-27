import unittest

import datetime

from app.main import db
from app.main.model.user import User
from app.test.base import BaseTestCase


class TestUserModel(BaseTestCase):

    def test_encode_auth_token(self):        
        user = User(
            nome='nometeste',
            login='test1@test.com',
            senha='test1'
        )        
        db.session.add(user)
        db.session.commit()
        auth_token = User.encode_auth_token(user.id)        
        self.assertTrue(isinstance(auth_token.encode('utf8'), bytes))

    def test_decode_auth_token(self):
        user = User(
            nome='nometeste2',
            login='test2@test.com',
            senha='test2',
        )
        db.session.add(user)
        db.session.commit()
        auth_token = User.encode_auth_token(user.id)        
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token.decode("utf-8") ) == 1)


if __name__ == '__main__':
    unittest.main()

