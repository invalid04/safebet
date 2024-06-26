from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db 
from .models import User
from flask_login import login_user, logout_user, login_required, current_user 
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect', category='error')
        else:
            flash('Username does not exist')

    return render_template("login.html")

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        username_exists = User.query.filter_by(username=username).first()

        if username_exists:
            flash('Username already in use', category='error')
        elif password1 != password2:
            flash('password don\'t match', category='error') 
        elif len(username) < 2:
            flash('Username is too short', category='error') 
        elif len(password1)  < 6:
            flash('password is too short', category='error')
        else:
            new_user = User(username=username, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created')
            return redirect(url_for('views.home'))
    
    return render_template("signup.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))