from app import app
from flaskext.mysql import MySQL
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'ope2'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ope2'
app.config['MYSQL_DATABASE_DB'] = 'OPE2'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)