import sqlite3
import os
import hashlib


DB_PATH = "app/users.db"

def db_connection():
    connection = sqlite3.connect(DB_PATH)
    return connection

def create_user(username, password, role):
    api_key = hashlib.sha256(os.urandom(24)).hexdigest()
    connection = db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password, api_key, role, reset_token) VALUES (?, ?, ?, ?, ?)",
                       (username, password, api_key, role, api_key))
        connection.commit()
    except sqlite3.IntegrityError as e:
        print(f"IntegrityError: {e}")
        return False
    finally:
        connection.close()

    return True


def find_user_by_username(username):
    connection = db_connection()
    cursor = connection.cursor()
    user = cursor.execute("SELECT * FROM users WHERE username = ?",
                          (username,)).fetchone()

    return user

def update_password(reset_token, password):
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute("""UPDATE users SET password = ? WHERE reset_token = ?""",
                   (password, reset_token))

    connection.commit()
    connection.close()

def set_reset_token(username, token):
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute("""UPDATE users SET reset_token = ? WHERE username = ?""",
                   (token, username))

    connection.commit()
    connection.close()

def validate_reset_token(token):
    connection = db_connection()
    cursor = connection.cursor()
    user = cursor.execute("""SELECT * FROM users WHERE reset_token = ?""",
                          (token,)).fetchone()

    connection.close()
    return user



