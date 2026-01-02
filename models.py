# Import necessary modules
# This file defines the database models for the expense tracking application.

from extensions import db 
from datetime import datetime
from flask_login import UserMixin

# Database Models
# User model to store user credentials for full financial compliance (KYC) and security

class User(UserMixin, db.Model):

    # This is the primary key for the User model
    id = db.Column(db.Integer, primary_key=True)
    
    # Account Security & Core Identity Fields
    # These fields are essential for user authentication and identification
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False) # For MFA
    dob = db.Column(db.Date, nullable=False) # For age verification
    
    # Compliance & Background Information
    # These fields are necessary for Know Your Customer (KYC) compliance
    home_address = db.Column(db.String(255), nullable=False)
    national_id = db.Column(db.String(50), unique=True, nullable=False)
    
    # Context-Specific Financial Fields (Optional)
    # These fields help tailor financial advice and services
    employment_status = db.Column(db.String(100))
    monthly_income = db.Column(db.Float)
    financial_goals = db.Column(db.Text)
    
    # Declarations & Consents
    # These boolean fields ensure users agree to terms and conditions
    terms_agreed = db.Column(db.Boolean, default=False)
    privacy_consent = db.Column(db.Boolean, default=False)
    data_accuracy_declaration = db.Column(db.Boolean, default=False)

    # Biometric/Security tracking
    # These fields enhance account security through biometric authentication
    biometric_id = db.Column(db.Text, nullable=True) 
    is_biometric_enabled = db.Column(db.Boolean, default=False)
    base_currency = db.Column(db.String(3), default='UGX')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships: Ensures expenses and budgets belong to this user
    # These relationships link the User model to Expense and Budget models
    expenses = db.relationship('Expense', backref='owner', lazy=True)
    budgets = db.relationship('Budget', backref='owner', lazy=True)

# Expense model to store individual expenses
class Expense(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    # Captures date and time for notifications
    date_to_handle = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_paid = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Budget model to store budget allocations per category
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    amount_allocated = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)