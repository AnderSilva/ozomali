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

@app.route('/user/add', methods=['POST'])
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

@app.route('/user', methods=['GET'])
def users():
	try:
		conn = db.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM Usuario")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/user/<int:id>', methods=['GET'])
def user(id):
	try:
		conn = db.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM Usuario WHERE id=%s", id)
		row = cursor.fetchone()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/user/update', methods=['PUT','POST'])
def update_user():
	try:
		_json = request.json
		_id = _json['id']
		_nome = _json['nome']
		_login = _json['login']
		_senha = _json['senha']
		# validate the received values
		if _nome and _login and _senha and _id and request.method == 'POST':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_senha)
			# save edits
			sql = "UPDATE Usuario SET nome=%s, login=%s, senha=%s WHERE id=%s"
			data = (_nome, _login, _senha, _id,)
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

@app.route('/user/delete/<int:id>', methods=['DELETE'])
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