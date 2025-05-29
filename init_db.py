from app import app, db
from auth import BankAdmin
import click
from getpass import getpass

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
        if not BankAdmin.query.filter_by(username='admin').first():
            print("Creating initial admin user...")
            username = input("Enter admin username (default: admin): ") or "admin"
            email = input("Enter admin email (default: admin@bank.com): ") or "admin@bank.com"
            password = getpass("Enter admin password: ")
            
            admin = BankAdmin(username=username, email=email, is_admin=True)
            admin.set_password(password)
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
        db.session.add_all(banks)
        db.session.commit()
        
        # Add sample users
        users = [
            User(name='John Doe', email='john@example.com', phone='1234567890', address='123 Main St, New York'),
            User(name='Jane Smith', email='jane@example.com', phone='0987654321', address='456 Park Ave, New York')
        ]
        db.session.add_all(users)
        db.session.commit()
        
        # Add sample accounts
        accounts = [
            Account(user_id=1, account_number='1001', balance=5000.00, account_type='savings'),
            Account(user_id=1, account_number='1002', balance=2500.00, account_type='checking'),
            Account(user_id=2, account_number='2001', balance=10000.00, account_type='savings')
        ]
        db.session.add_all(accounts)
        db.session.commit()
        
        # Add sample transactions
        transactions = [
            Transaction(account_id=1, amount=1000.00, transaction_type='deposit', timestamp=datetime.utcnow()),
            Transaction(account_id=2, amount=500.00, transaction_type='withdrawal', timestamp=datetime.utcnow()),
            Transaction(account_id=3, amount=2000.00, transaction_type='deposit', timestamp=datetime.utcnow())
        ]
        db.session.add_all(transactions)
        db.session.commit()
        
        # Add sample loans
        loans = [
            Loan(user_id=1, amount=10000.00, interest_rate=5.0, status='active'),
            Loan(user_id=2, amount=15000.00, interest_rate=4.5, status='active')
        ]
        db.session.add_all(loans)
        db.session.commit()

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
