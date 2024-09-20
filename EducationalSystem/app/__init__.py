import sqlite3
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    init_db()

    from EducationalSystem.app.controllers import auth_controller, file_controller
    app.register_blueprint(auth_controller.auth_bp)
    app.register_blueprint(file_controller.file_controller)

    return app


def init_db():
    db_path = "app/users.db"
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            user_token TEXT NOT NULL,
            role TEXT NOT NULL,
            reset_token TEXT
        )'''
    )
    connection.commit()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            uploader_id INTEGER NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            content BLOB,
            FOREIGN KEY (uploader_id) REFERENCES users (id)
        )'''
    )
    connection.commit()
    connection.close()
