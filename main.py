import ast
import operator
import os
import subprocess


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
	# Vulnerable: evaluates untrusted input.
	result = eval(expr)  # noqa: S307 (intentional for SAST exercise)
	print(f"Result: {result}")


def insecure_command():
	command = input("Enter a shell command: ")
	os.system(command)  # noqa: S602 (intentional for SAST exercise)


def main():
	insecure_login()
	dangerous_calculator()
	insecure_command()


if __name__ == "__main__":
	main()