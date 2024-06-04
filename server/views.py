from flask import Blueprint, render_template, jsonify, request 
from flask_login import login_required, current_user
from .models import User
from . import db

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


@login_required
@views.route('/bet', methods=['POST'])
def update_balance(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    bet_amount = data.get('amount')
    win_amount = data.get('win_amount')

    if not bet_amount or bet_amount <= 0:
        return jsonify({'error': 'Invalid bet amount'}), 400
    
    success = user.bet(bet_amount, win_amount)

    if success:
        db.session.commit()
        return jsonify({'message': 'Balance updated successfully'}), 200
    else:
        return jsonify({'error': 'Insufficient funds'}), 400