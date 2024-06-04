from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import User

views = Blueprint('views', __name__)

@views.route('/')
def home():
    user = current_user
    if user.is_authenticated:
        user_details = User.query.get(user.id)
        name = user_details.username 
        balance = user_details.balance
        return render_template('home.html', name=name, balance=balance)

    return render_template("home.html")

