import pymysql
from app import app
from db_config import db
from flask import jsonify
from flask import flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_expects_json import expects_json
from validate_schema.user_validate_schema import user_create_schema, user_auth_schema, user_update_schema
from validate_schema.provider_validate_schema import provider_create_schema, provider_update_schema
from validate_schema.product_validate_schema import product_create_schema, product_update_schema

@app.route('/', methods=['GET'])
def home():
	resp = jsonify('Bem vindo a ozomali-api v.0!!')
	resp.status_code = 200
	return resp

@app.route('/auth', methods=['POST'])
@expects_json(user_auth_schema)
def auth():
	try:
		_json = request.json
		_login = _json['login']
		_senha = _json['senha']	

		if _login and _senha and request.method == 'POST':
			engine = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'],{})
			conn = engine.raw_connection()

			cursor = conn.cursor(pymysql.cursors.DictCursor)
			sql = "SELECT senha FROM Usuario where login = '" + _login + "' "	

			cursor.execute(sql)
			values = cursor.fetchone()
		
			if values == None:
				resp = jsonify('Usuario nao foi autenticado!')
				resp.status_code = 401
				return resp
			_data = jsonify(values)
			_senhaHash = _data.json['senha']
			if not check_password_hash(_senhaHash, _senha):
				resp = jsonify('Usuario nao foi autenticado!')
				resp.status_code = 401
				return resp
			sql = "SELECT id, nome, login FROM Usuario where login = '" + _login + "' "	
			cursor.execute(sql)
			values = cursor.fetchone()	
			resp = jsonify(values)
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		if cursor is not None:
			cursor.close()
			conn.close()

@app.route('/users', methods=['POST'])
@expects_json(user_create_schema)
def add_user():
	try:
		_json = request.json
		_nome = _json['nome']
		_login = _json['login']
		_senha = _json['senha']

		if _nome and _login and _senha and request.method == 'POST':			
			_hash_senha = generate_password_hash(_senha)			
			sql = "INSERT INTO Usuario(nome, login, senha) VALUES(%s, %s, %s)"
			data = (_nome, _login, _hash_senha,)
			engine = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'],{})
			conn = engine.raw_connection()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User added successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/users/<int:id>', methods=['GET'])
@app.route('/users', methods=['GET'])
def users(id=0):
	try:
		_nome = request.args.get('nome')
		_login = request.args.get('login')
		_where = "" 
		if _nome:
			_where = " nome like '%" + _nome + "%' "
		if _login:
			_where = " login = '" + _login + "' "
		if id>0:
			_where += " id = " + str(id) + " "

		engine = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'],{})
		conn = engine.raw_connection()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		sql = "SELECT id, login, nome FROM Usuario"
		if _where :
			sql += " where " + _where
		cursor.execute(sql)
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		if cursor is not None:
			cursor.close()
			conn.close()

@app.route('/users', methods=['PUT'])
@expects_json(user_update_schema)
def update_user():
	try:
		_json = request.json
		_id = _json['id']
		_nome = _json['nome']
		_login = _json['login']
		_senha = _json['senha']
		# validate the received values
		if _nome and _login and _senha and _id and request.method == 'PUT':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_senha)
			# save edits
			sql = "UPDATE Usuario SET nome=%s, login=%s, senha=%s WHERE id=%s"
			data = (_nome, _login, _hashed_password, _id,)
			engine = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'],{})
			conn = engine.raw_connection()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('Usuario atualizado com sucesso!!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		if cursor is not None:
			cursor.close()
			conn.close()

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
	try:
		engine = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'],{})
		conn = engine.raw_connection()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("DELETE FROM Usuario WHERE id=%s", (id,))
		conn.commit()
		resp = jsonify('Usuario deletado com sucesso!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		if cursor is not None:
			cursor.close()
			conn.close()

@app.route('/providers', methods=['POST'])
@expects_json(provider_create_schema)
def add_provider():
	try:
		_json = request.json
		_nome = _json['nome']
		_cnpj = _json['cnpj']
		_cep = _json['cep']
		_endereco = _json['endereco']
		_numero = _json['numero']
		_complemento = ""
		if not (_json.get('complemento') is None):
			_complemento = _json['complemento']
		_cidade = _json['cidade']
		_estado = _json['estado']		

		if _nome and _cnpj and _cep and _endereco and _numero and _cidade and _estado and request.method == 'POST':						
			sql = "INSERT INTO Fornecedor(nome, cnpj, cep, endereco, numero, complemento, cidade, estado) VALUES(%s, %s, %s, %s,%s, %s, %s, %s)"
			data = (_nome, _cnpj, _cep, _endereco, _numero, _complemento, _cidade, _estado, )
			engine = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'],{})
			conn = engine.raw_connection()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('Fornecedor criado com sucesso!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		if cursor is not None:
			cursor.close()
			conn.close()

@app.route('/providers/<int:id>', methods=['GET'])
@app.route('/providers', methods=['GET'])
def providers(id=0):
	try:
		_nome = request.args.get('nome')
		_where = "" 
		if _nome:
			_where = " nome like '%" + _nome + "%' "
		if id>0:
			_where += " id = " + str(id) + " "
		engine = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'],{})
		conn = engine.raw_connection()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		sql = "SELECT * FROM Fornecedor"
		if _where :
			sql += " where " + _where
		cursor.execute(sql)
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		if cursor is not None:
			cursor.close()
			conn.close()

@app.route('/providers', methods=['PUT'])
@expects_json(provider_update_schema)
def update_provider():
	try:
		_json = request.json
		_id = _json['id']
		_nome = _json['nome']
		_cnpj = _json['cnpj']
		_cep = _json['cep']
		_endereco = _json['endereco']
		_numero = _json['numero']
		_complemento = _json['complemento']
		_cidade = _json['cidade']
		_estado = _json['estado']
		# validate the received values
		if _nome and _cnpj and _cep and _endereco and _numero and _cidade and _estado and _id and request.method == 'PUT':
			# save edits
			sql = "UPDATE Fornecedor SET nome=%s, cnpj=%s, cep=%s, endereco=%s, numero=%s, cidade=%s, estado=%s, complemento=%s WHERE id=%s"
			data = (_nome, _cnpj, _cep, _endereco, _numero, _cidade, _estado, _complemento, _id,)
			engine = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'],{})
			conn = engine.raw_connection()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('Fornecedor atualizado com sucesso!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		if cursor is not None:
			cursor.close()
			conn.close()

@app.route('/providers/<int:id>', methods=['DELETE'])
def delete_provider(id):
	try:
		engine = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'],{})
		conn = engine.raw_connection()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("DELETE FROM Fornecedor WHERE id=%s", (id,))
		conn.commit()
		resp = jsonify('Fornecedor deletado com sucesso!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		if cursor is not None:
			cursor.close()
			conn.close()

@app.route('/products', methods=['POST'])
@expects_json(product_create_schema)
def add_product():
	try:
		_json = request.json
		_nome = _json['nome']
		_preco_custo = _json['preco_custo']
		_preco_venda = _json['preco_venda']
		_quantidade = _json['quantidade']	

		if _nome and _preco_custo and _preco_venda and _quantidade and request.method == 'POST':						
			sql = "INSERT INTO Produto(nome, preco_custo, preco_venda, quantidade) VALUES(%s, %s, %s, %s )"
			data = (_nome, _preco_custo, _preco_venda, _quantidade, )
			engine = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'],{})
			conn = engine.raw_connection()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('Produto criado com sucesso!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		if cursor is not None:
			cursor.close()
			conn.close()

@app.route('/products/<int:id>', methods=['GET'])
@app.route('/products', methods=['GET'])
def products(id=0):
	try:
		_nome = request.args.get('nome')
		_where = ""
		if _nome:
			_where = " nome like '%" + _nome + "%' "
		if id>0:
			_where += " id = " + str(id) + " "
		engine = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'],{})
		conn = engine.raw_connection()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		sql = "SELECT * FROM Produto"
		if _where :
			sql += " where " +_where
		cursor.execute(sql)
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		if cursor is not None:
			cursor.close()
			conn.close()

@app.route('/products', methods=['PUT'])
@expects_json(product_update_schema)
def update_product():
	try:
		_json = request.json
		_id = _json['id']
		_nome = _json['nome']
		_preco_custo = _json['preco_custo']
		_preco_venda = _json['preco_venda']
		_quantidade = _json['quantidade']
		# validate the received values
		if _nome and _preco_custo and _preco_venda and _quantidade and _id and request.method == 'PUT':
			# save edits
			sql = "UPDATE Produto SET nome=%s, preco_custo=%s, preco_venda=%s, quantidade=%s WHERE id=%s"
			data = (_nome, _preco_custo, _preco_venda, _quantidade, _id,)
			engine = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'],{})
			conn = engine.raw_connection()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('Produto atualizado com sucesso!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		if cursor is not None:
			cursor.close()
			conn.close()

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
	try:
		engine = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'],{})
		conn = engine.raw_connection()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("DELETE FROM Produto WHERE id=%s", (id,))
		conn.commit()
		resp = jsonify('Produto deletado com sucesso!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		if cursor is not None:
			cursor.close()
			conn.close()

@app.errorhandler(404)
def not_found(error=None):
	message = {
		'status': 404,
		'message': 'Não encontrado: ' + request.url,
	}
	resp = jsonify(message)
	resp.status_code = 404

	return resp

if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True,port=5555)