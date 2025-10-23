import ast
import operator
import os
import subprocess


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


def get_user_password(username):
	passwords = {
		"admin": "admin123",  # Hard-coded credential.
		"user": "password",
	}
	return passwords.get(username, "changeme")


def insecure_login():
	username = input("Username: ")
	password = input("Password: ")
	stored = get_user_password(username)
	if stored == password:
		print("Login successful")
	else:
		print("Access denied")


def dangerous_calculator():
	expr = input("Enter a math expression: ")
	try:
		parsed = ast.parse(expr, mode="eval")
		result = _safe_eval(parsed.body)
		print(f"Result: {result}")
	except Exception:
		print("Invalid expression supplied.")


def insecure_command():
	command = input("Enter a shell command: ")
	allowed = {
		"dir": ["cmd", "/c", "dir"],
		"ls": ["ls"],
	}
	if command in allowed:
		try:
			subprocess.run(allowed[command], check=True)
		except subprocess.CalledProcessError:
			print("Command failed.")
	else:
		print("Command blocked.")


def main():
	insecure_login()
	dangerous_calculator()
	insecure_command()


if __name__ == "__main__":
	main()