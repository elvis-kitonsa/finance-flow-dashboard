from extensions import db
from datetime import datetime

# Database Models
# User model to store user credentials and preferences

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    # This field will store public keys for Biometric/WebAuthn login
    biometric_id = db.Column(db.Text, nullable=True) 
    base_currency = db.Column(db.String(3), default='USD')

# Expense model to store individual expenses
class Expense(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    # Captures date and time for notifications as you requested
    date_to_handle = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_paid = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Budget model to store budget allocations per category
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    amount_allocated = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)