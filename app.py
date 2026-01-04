from flask import Flask, render_template, request, jsonify
from extensions import db # Importing the db instance from extensions.py
from datetime import datetime
import os

app = Flask(__name__)

# Basic Configuration
app.config['SECRET_KEY'] = 'your-very-secret-key'
# Note: SQLite stores the file in the 'instance' folder by default in newer Flask versions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
# This line connects the Flask app with the SQLAlchemy instance
# and allows us to use the models defined in models.py

db.init_app(app)

# Import models AFTER db is defined to avoid circular imports
from models import User, Expense, Budget

@app.route('/')
def dashboard():
    # 1. Fetch the admin user
    user = User.query.filter_by(email="admin@financeflow.com").first()
    
    # 2. Get the balance from the database (fallback to 0 if user is missing)
    balance_to_show = user.total_balance if user else 0
    
    # 3. Fetch expenses
    all_expenses = Expense.query.order_by(Expense.date_to_handle.desc()).all()
    
    # 4. Pass 'total_balance' to the template
    return render_template('dashboard.html', 
                           expenses=all_expenses, 
                           total_balance=balance_to_show)

# THIS IS THE MISSING ROUTE
@app.route('/add_expense', methods=['POST'])
def add_expense():
    try:
        data = request.get_json()
        
        # Create the new record
        new_expense = Expense(
            title=data['title'],
            amount=float(data['amount']),
            category=data['category'],
            # This converts the text from the HTML picker into a Python Date object
            date_to_handle=datetime.strptime(data['date'], '%Y-%m-%dT%H:%M'),
            user_id=1 # Temporary hardcode until we build the login portal
        )
        
        db.session.add(new_expense)
        db.session.commit()
        
        return jsonify({"message": "Expense saved successfully!"}), 200
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Internal Server Error"}), 500

# 
from werkzeug.security import generate_password_hash
from datetime import date

# Initialize the database and create admin user if not exists
with app.app_context():
    db.create_all()

    # Create admin user if memory is empty
    # Updated to match your new model fields
    if not User.query.filter_by(email="admin@financeflow.com").first():
        admin = User(
            email="admin@financeflow.com",
            password_hash=generate_password_hash("admin123"),
            full_name="Admin User",
            phone="000000000",
            dob=date(1990, 1, 1),
            home_address="System",
            national_id="ADMIN-001",
            terms_agreed=True,
            privacy_consent=True,
            data_accuracy_declaration=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Database initialized and Admin created!")

@app.route('/update_balance', methods=['POST'])
def update_balance():
    data = request.get_json()
    # Use the email to find the user instead of ID 1 to be 100% sure
    user = User.query.filter_by(email="admin@financeflow.com").first() 
    if user:
        user.total_balance = float(data['balance'])
        db.session.commit()
        return jsonify({"status": "success", "new_balance": user.total_balance})
    return jsonify({"status": "error"}), 404

if __name__ == '__main__':
    app.run(debug=True)
