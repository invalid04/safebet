from . import db 
from flask_login import UserMixin 
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    balance = db.Column(db.Integer, default=500)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    def bet(self, amount, win_amount):
        if self.balance >= amount:
            self.balance -= amount 
            self.balance += win_amount
            db.session.commit() 
            return True 
        else:
            return False