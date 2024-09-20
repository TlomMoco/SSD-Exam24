import datetime
import os
import jwt
import bcrypt
import bleach
from functools import wraps
from flask import render_template, request, redirect, url_for, session, flash, Blueprint
from EducationalSystem.app.models import user_model
from EducationalSystem.app.models import file_model


auth_bp = Blueprint('auth_bp', __name__)


# Decorator for session based authentication
def login_required(f):
    @wraps(f)
    def decorator_function(*args, **kwargs):
        user_id = session.get("user_id")
        if not user_id:
            flash("You need to be logged in to view this page.", "error")
            return redirect(url_for('auth_bp.login'))
        return f(*args, **kwargs)
    return decorator_function


@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Find user in db by username
        user = user_model.find_user_by_username(username)

        if user and password_verification(user[2], password):
            # Storing values in session
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['user_token'] = user[3]
            session['role'] = user[4]

            return redirect(url_for('auth_bp.dashboard'))
        else:
            flash("Invalid credentials.", "error")
    return render_template("LoginPage.html")

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('auth_bp.login'))

@auth_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    username = session.get("username")
    role = session.get("role")
    files = file_model.get_all_files()
    return render_template("DashboardPage.html", username=username, role=role, files=files)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        # Sanitizing inputs
        username = bleach.clean(username, tags=[], attributes={}, strip=True)
        role = bleach.clean(role, tags=[], attributes={}, strip=True)

        hashed_password = password_encryption(password)
        if username == "" or password == "" or role == "":
            flash("User credentials must be filled out", "error")
            return redirect(url_for('auth_bp.register_user'))
        if user_model.create_user(username, hashed_password, role):
            flash("Registration successful!", "success")
            return redirect(url_for('auth_bp.login'))
        else:
            flash("Registration failed!", "error")
    return render_template("RegistrationPage.html")


# This would normally be handled with a 2FA where you could send the password via SMTP
# But I didn't have the time to fix that, so here is an emergency solution
def generate_reset_token(user):
    payload = {
        "user_id": user[0],
        "exp": datetime.datetime.now() + datetime.timedelta(minutes=60) # token expires in 60m
    }
    token = jwt.encode(payload, os.getenv('SECRET_KEY', 'secret_key_for_this_educational_system'), algorithm='HS256')
    return token

@auth_bp.route('/request_reset', methods=['GET', 'POST'])
def request_reset():
    if request.method == 'POST':
        username = request.form.get('username')
        user = user_model.find_user_by_username(username)
        if user:
            token = generate_reset_token(user)
            user_model.set_reset_token(user[0], token)
            return redirect(url_for('auth_bp.show_reset_token', token=token))
        else:
            flash("Invalid credentials.", "error")
    return render_template("RequestResetPage.html")

@auth_bp.route('/show_reset_token/<token>', methods=['GET', 'POST'])
def show_reset_token(token):
    return render_template("ShowResetToken.html", token=token)

# Password update after reset
@auth_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'GET':
        return render_template("ResetPasswordPage.html")

    if request.method == 'POST':
        token = request.form['token']
        new_password = request.form['password']

        if token == "" or new_password == "":
            flash("Invalid input.", "error")
            return render_template("ResetPasswordPage.html")

        user = user_model.validate_reset_token(token)
        if user:
            hashed_password = password_encryption(new_password)
            user_model.update_password(token, hashed_password)
            #user_model.clear_user_token(user[0], token)
            flash("Password updated successfully!", "success")
            return redirect(url_for('auth_bp.login'))
        else:
            flash("Invalid or expired token.", "error")
            return render_template("ResetPasswordPage.html")
    render_template("ResetPasswordPage.html")


# Helper functions for encrypting and decrypting password
def password_verification(hashed_password, entered_password) -> bool:
    return bcrypt.checkpw(entered_password.encode(), hashed_password)

def password_encryption(password):
    bcrypt_hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return bcrypt_hashed_password
