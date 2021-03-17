import pymysql
from app import app
from db_config import db
from flask import jsonify
from flask import flash, request
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/', methods=['GET'])
def home():
	resp = jsonify('Bem vindo a ozomali-api v.0!!')
	resp.status_code = 200
	return resp

@app.route('/users', methods=['POST'])
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
			conn = db.connect()
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

@app.route('/users', methods=['GET'])
def users():
	try:
		_nome = request.args.get('nome')
		_where = "" 
		if _nome:
			_where = " nome like '%" + _nome + "%' "		

		conn = db.connect()
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
		cursor.close()
		conn.close()

@app.route('/users/<int:id>', methods=['GET'])
def userById(id):
	try:
		conn = db.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT id, login, nome FROM Usuario WHERE id=%s", id)
		row = cursor.fetchone()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/users', methods=['PUT'])
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
			conn = db.connect()
			cursor = conn.cursor()
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
		cursor.close()
		conn.close()

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
	try:
		conn = db.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM Usuario WHERE id=%s", (id,))
		conn.commit()
		resp = jsonify('Usuario deletado com sucesso!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/providers', methods=['POST'])
def add_provider():
	try:
		_json = request.json
		_nome = _json['nome']
		_cnpj = _json['cnpj']
		_cep = _json['cep']
		_endereco = _json['endereco']
		_numero = _json['numero']
		_complemento = _json['complemento']
		_cidade = _json['cidade']
		_estado = _json['estado']		

		if _nome and _cnpj and _cep and _endereco and _numero and _cidade and _estado and request.method == 'POST':						
			sql = "INSERT INTO Fornecedor(nome, cnpj, cep, endereco, numero, complemento, cidade, estado) VALUES(%s, %s, %s, %s,%s, %s, %s, %s)"
			data = (_nome, _cnpj, _cep, _endereco, _numero, _complemento, _cidade, _estado, )
			conn = db.connect()
			cursor = conn.cursor()
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
		cursor.close()
		conn.close()

@app.route('/providers', methods=['GET'])
def providers():
	try:
		_nome = request.args.get('nome')
		_where = "" 
		if _nome:
			_where = " nome like '%" + _nome + "%' "

		conn = db.connect()
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
		cursor.close()
		conn.close()

@app.route('/providers/<int:id>', methods=['GET'])
def provider(id):
	try:
		conn = db.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM Fornecedor WHERE id=%s", id)
		row = cursor.fetchone()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/providers', methods=['PUT'])
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
			conn = db.connect()
			cursor = conn.cursor()
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
		cursor.close()
		conn.close()

@app.route('/providers/<int:id>', methods=['DELETE'])
def delete_provider(id):
	try:
		conn = db.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM Fornecedor WHERE id=%s", (id,))
		conn.commit()
		resp = jsonify('Fornecedor deletado com sucesso!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/products', methods=['POST'])
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
			conn = db.connect()
			cursor = conn.cursor()
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
		cursor.close()
		conn.close()

@app.route('/products', methods=['GET'])
def products():
	try:
		_nome = request.args.get('nome')
		_where = ""
		if _nome:
			_where = " nome like '%" + _nome + "%' "

		conn = db.connect()
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
		cursor.close()
		conn.close()

@app.route('/products/<int:id>', methods=['GET'])
def product(id):
	try:
		conn = db.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM Produto WHERE id=%s", id)
		row = cursor.fetchone()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/products', methods=['PUT'])
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
			conn = db.connect()
			cursor = conn.cursor()
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
		cursor.close()
		conn.close()

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
	try:
		conn = db.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM Produto WHERE id=%s", (id,))
		conn.commit()
		resp = jsonify('Produto deletado com sucesso!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
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