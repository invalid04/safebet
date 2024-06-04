from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "login"

@auth.route('/sign-up')
def sign_up():
    return "signup"

@auth.route('/logout')
def logout():
    return "logout"