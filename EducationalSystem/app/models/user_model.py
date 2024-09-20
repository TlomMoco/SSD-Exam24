import sqlite3
import os
import hashlib


DB_PATH = "app/users.db"

def db_connection():
    connection = sqlite3.connect(DB_PATH)
    return connection

def create_user(username, password, role):
    user_token = hashlib.sha256(os.urandom(24)).hexdigest()
    connection = db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password, user_token, role, reset_token) VALUES (?, ?, ?, ?, ?)",
                       (username, password, user_token, role, None))
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
    cursor.execute("""UPDATE users SET password = ?, reset_token = NULL WHERE reset_token = ?""",
                   (password, reset_token))
    connection.commit()
    connection.close()

def set_user_token(user_id, user_token):
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE users SET user_token = ? WHERE id = ?""",
                   (user_token, user_id))
    connection.commit()
    connection.close()

def clear_user_token(user_id, user_token):
    set_user_token(user_id, None)

def find_user_token(user_token):
    connection = db_connection()
    cursor = connection.cursor()
    user = cursor.execute("SELECT * FROM users WHERE user_token = ?",
                          (user_token,)).fetchone()
    connection.close()
    return user

def set_reset_token(user_id, token):
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute("""UPDATE users SET reset_token = ? WHERE id = ?""",
                   (token, user_id))
    connection.commit()
    connection.close()

def validate_reset_token(token):
    connection = db_connection()
    cursor = connection.cursor()
    user = cursor.execute("""SELECT * FROM users WHERE reset_token = ?""",
                          (token,)).fetchone()
    connection.close()
    return user

