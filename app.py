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
    
    # Fetch all expenses from the database, newest first
    all_expenses = Expense.query.order_by(Expense.date_to_handle.desc()).all()
    return render_template('dashboard.html', expenses=all_expenses)

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

# Initialize the database and create admin user if not exists
with app.app_context():
    db.create_all()
    # Create admin user if memory is empty
    if not User.query.get(1):
        db.session.add(User(username="admin", password_hash="123"))
        db.session.commit()
        print("Database initialized successfully!")

if __name__ == '__main__':
    app.run(debug=True)
