from flask import Flask, render_template, request, redirect, url_for, session, flash, abort, Blueprint
from EducationalSystem.app.models import user_model
import os
import hashlib


auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = user_model.find_user_by_username(username)

        # If user exists and password is correct
        # Implement bcrypt instead of werkzeug.security to hash the password and check it
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session['api_key'] = user.api_key
