import sqlite3
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    init_db()

    from EducationalSystem.app.controllers import auth_controller, file_controller, user_controller
    app.register_blueprint(auth_controller.auth_bp)
    app.register_blueprint(file_controller)
    app.register_blueprint(user_controller)

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
            api_key TEXT NOT NULL,
            role TEXT NOT NULL,
            reset_token TEXT
        )'''
    )
    connection.commit()
    connection.close()
