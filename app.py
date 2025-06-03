from flask import Flask, jsonify, render_template, redirect, url_for, flash, request # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_login import login_required, current_user, login_user, logout_user # type: ignore
from datetime import datetime
from models import db, User, Account, Transaction, Loan, LoanPayment, BankAdmin
from auth import init_login_manager

app = Flask(__name__)   
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'

db.init_app(app)
init_login_manager(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        user = BankAdmin.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        if request.form['password'] != request.form['confirm_password']:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')
        
        if BankAdmin.query.filter_by(username=request.form['username']).first():
            flash('Username already exists.', 'danger')
            return render_template('register.html')
            
        if BankAdmin.query.filter_by(email=request.form['email']).first():
            flash('Email already registered.', 'danger')
            return render_template('register.html')
            
        user = BankAdmin(username=request.form['username'], email=request.form['email'])
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    user_count = User.query.count()
    account_count = Account.query.count()
    loan_count = Loan.query.filter(Loan.status.in_(['approved', 'pending'])).count()
    
    # Calculate total balance across all accounts
    total_balance = db.session.query(db.func.sum(Account.balance)).scalar() or 0
    
    recent_loans = Loan.query.order_by(Loan.application_date.desc()).limit(5).all()
    recent_transactions = Transaction.query.order_by(Transaction.timestamp.desc()).limit(5).all()
    
    return render_template('index.html',
                         user_count=user_count,
                         account_count=account_count,
                         loan_count=loan_count,
                         total_balance=total_balance,
                         recent_transactions=recent_transactions,
                         recent_loans=recent_loans)

# Loan routes
@app.route('/loans')
@login_required
def loans():
    loans = Loan.query.order_by(Loan.application_date.desc()).all()
    users = User.query.all()  # Add this for the modal form
    return render_template('loans.html', loans=loans, users=users)

@app.route('/loans/apply', methods=['GET', 'POST'])
@login_required
def apply_loan():
    if request.method == 'POST':
        loan = Loan(
            user_id=request.form['user_id'],
            amount=float(request.form['amount']),
            interest_rate=float(request.form['interest_rate']),
            purpose=request.form['purpose'],
            status='pending',
            monthly_payment=float(request.form['amount']) * (float(request.form['interest_rate'])/1200) / (1 - (1 + float(request.form['interest_rate'])/1200)**(-int(request.form['term'])))
        )
        db.session.add(loan)
        db.session.commit()
        flash('Loan application submitted successfully!', 'success')
        return redirect(url_for('loans'))
    
    users = User.query.all()
    return render_template('loan_application.html', users=users)

@app.route('/loans/<int:loan_id>/approve', methods=['POST'])
@login_required
def approve_loan(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    loan.status = 'approved'
    loan.approval_date = datetime.utcnow()
    db.session.commit()
    flash('Loan approved successfully!', 'success')
    return redirect(url_for('loans'))

@app.route('/loans/<int:loan_id>/reject', methods=['POST'])
@login_required
def reject_loan(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    loan.status = 'rejected'
    db.session.commit()
    flash('Loan rejected successfully!', 'success')
    return redirect(url_for('loans'))

@app.route('/loans/<int:loan_id>/payment', methods=['POST'])
@login_required
def make_payment(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    payment = LoanPayment(
        loan_id=loan.id,
        amount=float(request.form['amount'])
    )
    db.session.add(payment)
    
    # Check if loan is fully paid
    total_paid = sum(payment.amount for payment in loan.payments)
    if total_paid >= loan.amount:
        loan.status = 'paid'
    
    db.session.commit()
    flash('Payment processed successfully!', 'success')
    return redirect(url_for('loans'))

# Account and transaction routes for dashboard functionality
@app.route('/accounts')
@login_required
def accounts():
    accounts = Account.query.all()
    return render_template('accounts.html', accounts=accounts)

@app.route('/transactions')
@login_required
def transactions():
    transactions = Transaction.query.order_by(Transaction.timestamp.desc()).all()
    return render_template('transactions.html', transactions=transactions)

# Simplified API endpoints for AJAX operations
@app.route('/api/loans/<int:loan_id>', methods=['GET'])
@login_required
def get_loan_details(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    payments = LoanPayment.query.filter_by(loan_id=loan_id).order_by(LoanPayment.payment_date.desc()).all()
    return jsonify({
        'loan': {
            'id': loan.id,
            'amount': loan.amount,
            'interest_rate': loan.interest_rate,
            'monthly_payment': loan.monthly_payment,
            'status': loan.status,
            'purpose': loan.purpose,
            'application_date': loan.application_date.isoformat(),
            'approval_date': loan.approval_date.isoformat() if loan.approval_date else None
        },
        'payments': [{
            'id': payment.id,
            'amount': payment.amount,
            'date': payment.payment_date.isoformat()
        } for payment in payments]
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create admin user if not exists
        if not BankAdmin.query.filter_by(username='admin').first():
            admin = BankAdmin(username='admin', email='admin@bank.com', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)
