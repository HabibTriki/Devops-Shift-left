# import ast
# import operator
# import os
# import subprocess


# _ALLOWED_BIN_OPS = {
# 	ast.Add: operator.add,
# 	ast.Sub: operator.sub,
# 	ast.Mult: operator.mul,
# 	ast.Div: operator.truediv,
# 	ast.Mod: operator.mod,
# 	ast.Pow: operator.pow,
# }


# def _safe_eval(node):
# 	if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
# 		return node.value
# 	if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BIN_OPS:
# 		return _ALLOWED_BIN_OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
# 	if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
# 		return +_safe_eval(node.operand) if isinstance(node.op, ast.UAdd) else -_safe_eval(node.operand)
# 	raise ValueError("Disallowed expression")


# def get_user_password(username):
# 	# ...existing code...
# 	passwords = {
# 		"admin": "admin123",  # Hard-coded credential.
# 		"user": "password",
# 	}
# 	return passwords.get(username, "changeme")


# def insecure_login():
# 	# ...existing code...
# 	username = input("Username: ")
# 	password = input("Password: ")
# 	stored = get_user_password(username)
# 	if stored == password:
# 		print("Login successful")
# 	else:
# 		print("Access denied")


# def dangerous_calculator():
# 	expr = input("Enter a math expression: ")
# 	try:
# 		parsed = ast.parse(expr, mode="eval")
# 		result = _safe_eval(parsed.body)
# 		print(f"Result: {result}")
# 	except Exception:
# 		print("Invalid expression supplied.")


# def insecure_command():
# 	command = input("Enter a shell command: ")
# 	allowed = {
# 		"dir": ["cmd", "/c", "dir"],
# 		"ls": ["ls"],
# 	}
# 	if command in allowed:
# 		try:
# 			subprocess.run(allowed[command], check=True)
# 		except subprocess.CalledProcessError:
# 			print("Command failed.")
# 	else:
# 		print("Command blocked.")


# def main():
# 	insecure_login()
# 	dangerous_calculator()
# 	insecure_command()


# if __name__ == "__main__":
# 	main()

# main.py
import os
import ast
import operator
from flask import Flask, request, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Allowed operations for safe evaluator
_ALLOWED_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
def _safe_eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BIN_OPS:
        return _ALLOWED_BIN_OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        return +_safe_eval(node.operand) if isinstance(node.op, ast.UAdd) else -_safe_eval(node.operand)
    raise ValueError("Disallowed expression")

# Credentials: use environment variable for the password hash
# To set in Docker: ADMIN_PASSWORD_HASH='<hash>'
DEFAULT_PW = "admin123"  # only used if no env var provided (not recommended for prod)
_admin_hash = os.getenv("ADMIN_PASSWORD_HASH")
if not _admin_hash:
    # Generate a hash from default for convenience (only for demo). Prefer injecting ADMIN_PASSWORD_HASH.
    _admin_hash = generate_password_hash(DEFAULT_PW)

@app.route("/", methods=["GET"])
def root():
    return jsonify({"status": "ok", "endpoints": ["/health", "/login", "/calc"]}), 200

@app.route("/favicon.ico")
def favicon():
    return ("", 204)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return jsonify({
            "info": "POST to this endpoint with JSON",
            "example": {
                "username": "admin",
                "password": "your_password"
            }
        }), 200
    
    data = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")

    # Example user store: in real projects, use a DB with hashed passwords and proper auth
    # Here we only support a single admin user for the exercise
    if username != "admin":
        return jsonify({"ok": False, "reason": "invalid username"}), 401

    if check_password_hash(_admin_hash, password):
        return jsonify({"ok": True, "message": "login successful"}), 200
    else:
        return jsonify({"ok": False, "reason": "invalid credentials"}), 401

@app.route("/calc", methods=["GET", "POST"])
def calc():
    if request.method == "GET":
        return jsonify({
            "info": "POST to this endpoint with JSON",
            "example": {
                "expr": "2 + 3 * 4"
            }
        }), 200
    
    data = request.get_json(silent=True) or {}
    expr = data.get("expr", "")
    if not expr:
        return jsonify({"ok": False, "reason": "no expression provided"}), 400

    # parse & evaluate safely
    try:
        parsed = ast.parse(expr, mode="eval")
        result = _safe_eval(parsed.body)
        return jsonify({"ok": True, "result": result}), 200
    except Exception as e:
        return jsonify({"ok": False, "reason": "invalid expression", "detail": str(e)}), 400

if __name__ == "__main__":
    # host and port must match Dockerfile expectation (0.0.0.0:5000)
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
