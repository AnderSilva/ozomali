# ozomali
Repositório do Grupo de OPE2

Requisitos 
Python 3
Mariadb


Chamada da api
Está em criação um swagger para a documentaçao da API, aguardem :) 

https://ozomali-api.herokuapp.com/


Instalação para run local:

* virtualenv -p `which python3` venv
* source venv/bin/activate
* pip install -r requirements.txt

crie o arquivo .env na raiz do projeto com as informações do mariadb:
    MYSQL_DATABASE_USER = 'informar_user_db'
    MYSQL_DATABASE_PASSWORD = 'senha_do_user'
    MYSQL_DATABASE_DB = 'nome_do_database'
    MYSQL_DATABASE_HOST = 'host_do_mysql/mariadb'

* gunicorn --pythonpath backend main:app
