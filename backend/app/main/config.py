import os
basedir = os.path.abspath(os.path.dirname(__file__))
from dotenv import load_dotenv
load_dotenv()

postgresql_base = os.getenv('SQLALCHEMY_DATABASE_URI')
postgresql_base_dev = os.getenv('SQLALCHEMY_DATABASE_URI_DEV')
postgresql_base_tst = 'sqlite:///' + os.path.join(basedir, 'ozomali_test.db')    

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'CODIGO_SECRETO_OZOMALI_NONE_ATIVAR')
    SRF_ENABLED = True    


class DevelopmentConfig(Config):    
    SQLALCHEMY_DATABASE_URI = postgresql_base_dev
    SECRET_KEY = 'CODIGO_SECRETO_OZOMALI_DEV_ATIVAR'
    DEBUG = True    
    SQLALCHEMY_ECHO = False    
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = postgresql_base_tst
    SECRET_KEY = 'CODIGO_SECRETO_OZOMALI_TESTE_ATIVAR'
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = postgresql_base
    DEBUG = False
        

config_by_name = dict(
    dev=DevelopmentConfig,
    tst=TestingConfig,
    prd=ProductionConfig
)

key = Config.SECRET_KEY
