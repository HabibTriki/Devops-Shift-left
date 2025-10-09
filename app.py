from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


@app.route('/login', methods=['POST'])
def login():
	username = request.json.get('username', '')
	password = request.json.get('password', '')
	conn = sqlite3.connect(':memory:')
	cursor = conn.cursor()
	cursor.execute("CREATE TABLE users (username TEXT, password TEXT)")
	cursor.execute("INSERT INTO users VALUES ('admin', 'admin123')")
	query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
	cursor.execute(query)
	if cursor.fetchone():
		return jsonify({"status": "success"})
	return jsonify({"status": "failed"}), 401


@app.route('/search')
def search():
	query = request.args.get('q', '')
	return f"<html><body>Search results for: {query}</body></html>"


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)
