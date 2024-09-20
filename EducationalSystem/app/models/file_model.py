from flask import current_app
from datetime import datetime
import os
import sqlite3

def db_connection():
    db_path = os.path.join(current_app.root_path, "users.db")
    connection = sqlite3.connect(db_path)
    return connection

def save_file_metadata(filename, uploader_id, content):
    connection = db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO files (filename, uploader_id, uploaded_at, content) VALUES (?, ?, ?, ?)""",
                       (filename, uploader_id, datetime.now(), content))
        connection.commit()
    except sqlite3.Error as e:
        print(f"Error saving file: {e}")
    finally:
        connection.close()

def get_file_content(filename):
    connection = db_connection()
    cursor = connection.cursor()
    try:
        file_row = cursor.execute("""
        SELECT content FROM files WHERE filename = ?""",
                   (filename,))
        file_content = file_row.fetchone()
        if file_content:
            return file_content[0]
        else:
            return None

    except sqlite3.Error as e:
        print(f"Error getting file: {e}")
    finally:
        cursor.close()
        connection.close()



def get_all_files():
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT * FROM files
        """)
    files = cursor.fetchall()
    connection.close()
    return files