from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Account, Transaction, Loan, LoanPayment, BankAdmin
import click
from getpass import getpass
from datetime import datetime
import os

# Create a Flask application context
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'banking.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'

# Ensure the instance folder exists
instance_path = os.path.join(basedir, 'instance')
os.makedirs(instance_path, exist_ok=True)

# Initialize the database with the app
db.init_app(app)

def init_db():
    with app.app_context():
        print("Initializing database...")
        db.create_all()
        print("Tables created successfully!")
        
        # Create initial admin user if it doesn't exist
        if not BankAdmin.query.filter_by(username='admin').first():
            print("\nCreating initial admin user...")
            username = input("Enter admin username (default: admin): ") or "admin"
            email = input("Enter admin email (default: admin@bank.com): ") or "admin@bank.com"
            password = getpass("Enter admin password: ")
            
            admin = BankAdmin(username=username, email=email, is_admin=True)
            admin.set_password(password)
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
        
        # Add sample users
        if User.query.count() == 0:
            print("\nCreating sample users...")
            users = [
                User(name='John Doe', email='john@example.com', phone='1234567890'),
                User(name='Jane Smith', email='jane@example.com', phone='0987654321')
            ]
            db.session.add_all(users)
            db.session.commit()
            print("Sample users created successfully!")
            
            # Add sample accounts
            print("\nCreating sample accounts...")
            accounts = [
                Account(user_id=1, account_number='1001', balance=5000.00, account_type='savings'),
                Account(user_id=1, account_number='1002', balance=2500.00, account_type='checking'),
                Account(user_id=2, account_number='2001', balance=10000.00, account_type='savings')
            ]
            db.session.add_all(accounts)
            db.session.commit()
            print("Sample accounts created successfully!")
            
            # Add sample transactions
            print("\nCreating sample transactions...")
            transactions = [
                Transaction(account_id=1, amount=1000.00, transaction_type='deposit'),
                Transaction(account_id=2, amount=500.00, transaction_type='withdrawal'),
                Transaction(account_id=3, amount=2000.00, transaction_type='deposit')
            ]
            db.session.add_all(transactions)
            db.session.commit()
            print("Sample transactions created successfully!")
            
            # Add sample loans
            print("\nCreating sample loans...")
            loans = [
                Loan(user_id=1, amount=10000.00, interest_rate=5.0, purpose='Home renovation',
                     status='approved', monthly_payment=188.71, approval_date=datetime.utcnow()),
                Loan(user_id=2, amount=5000.00, interest_rate=7.5, purpose='Business expansion',
                     status='pending', monthly_payment=100.87)
            ]
            db.session.add_all(loans)
            db.session.commit()
            print("Sample loans created successfully!")

@click.group()
def cli():
    """Banking System Database Management CLI"""
    pass

@cli.command()
def init():
    """Initialize the database and create admin user"""
    init_db()

@cli.command()
def reset():
    """Reset the database (Warning: This will delete all data)"""
    if input("Are you sure you want to reset the database? (y/N): ").lower() == 'y':
        with app.app_context():
            db.drop_all()
            db.create_all()
            print("Database reset successfully!")
    else:
        print("Database reset cancelled.")

if __name__ == '__main__':
    cli()
