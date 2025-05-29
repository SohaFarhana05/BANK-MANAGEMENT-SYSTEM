from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user, login_user, logout_user
from datetime import datetime
from models import db, Bank, User, Account, Transaction, Loan, Payment, Branch
from auth import BankAdmin, init_login_manager
app = Flask(__name__)   
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'  # Required for flash messages
db.init_app(app)
init_login_manager(app)

with app.app_context():
    db.create_all()
    # Create admin user if not exists
    if not BankAdmin.query.filter_by(username='admin').first():
        admin = BankAdmin(username='admin', email='admin@bank.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()

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

@app.route('/banks', methods=['POST'])
def create_bank():
    data = request.get_json()
    new_bank = Bank(name=data['name'], location=data['location'])
    db.session.add(new_bank)
    db.session.commit()
    return jsonify({'message': 'Bank created successfully!'}), 201
@app.route('/users', methods=['POST'])
def create_user():
    if request.form:
        data = request.form
    else:
        data = request.get_json()
    
    new_user = User(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        address=data.get('address', 'Not provided')  # Make address optional
    )
    db.session.add(new_user)
    db.session.commit()
    
    if request.form:
        flash('User created successfully!', 'success')
        return redirect(url_for('users'))
    return jsonify({'message': 'User created successfully!'}), 201
@app.route('/accounts', methods=['POST'])
def create_account():
    data = request.get_json()
    new_account = Account(user_id=data['user_id'], account_number=data['account_number'], balance=data['balance'], account_type=data['account_type'])
    db.session.add(new_account)
    db.session.commit()
    return jsonify({'message': 'Account created successfully!'}), 201
@app.route('/transactions', methods=['POST'])
def create_transaction():
    data = request.get_json()
    new_transaction = Transaction(account_id=data['account_id'], amount=data['amount'], transaction_type=data['transaction_type'], timestamp=datetime.utcnow())
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction created successfully!'}), 201
@app.route('/loans', methods=['POST'])
def create_loan():
    data = request.get_json()
    new_loan = Loan(user_id=data['user_id'], amount=data['amount'], interest_rate=data['interest_rate'], status=data['status'])
    db.session.add(new_loan)
    db.session.commit()
    return jsonify({'message': 'Loan created successfully!'}), 201
@app.route('/payments', methods=['POST'])
def create_payment():
    data = request.get_json()
    new_payment = Payment(loan_id=data['loan_id'], amount=data['amount'], payment_date=datetime.utcnow())
    db.session.add(new_payment)
    db.session.commit()
    return jsonify({'message': 'Payment created successfully!'}), 201
@app.route('/branches', methods=['POST'])
def create_branch():
    data = request.get_json()
    new_branch = Branch(bank_id=data['bank_id'], name=data['name'], location=data['location'])
    db.session.add(new_branch)
    db.session.commit()
    return jsonify({'message': 'Branch created successfully!'}), 201
@app.route('/banks', methods=['GET'])
def get_banks():
    banks = Bank.query.all()
    return jsonify([{'id': bank.id, 'name': bank.name, 'location': bank.location} for bank in banks]), 200
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name, 'email': user.email, 'phone': user.phone} for user in users]), 200
@app.route('/accounts', methods=['GET'])    
def get_accounts():
    accounts = Account.query.all()
    return jsonify([{'id': account.id, 'user_id': account.user_id, 'account_number': account.account_number, 'balance': account.balance, 'account_type': account.account_type} for account in accounts]), 200
@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    return jsonify([{'id': transaction.id, 'account_id': transaction.account_id, 'amount': transaction.amount, 'transaction_type': transaction.transaction_type, 'timestamp': transaction.timestamp} for transaction in transactions]), 200
@app.route('/loans', methods=['GET'])
def get_loans():
    loans = Loan.query.all()
    return jsonify([{'id': loan.id, 'user_id': loan.user_id, 'amount': loan.amount, 'interest_rate': loan.interest_rate, 'status': loan.status} for loan in loans]), 200
@app.route('/payments', methods=['GET'])
def get_payments():
    payments = Payment.query.all()
    return jsonify([{'id': payment.id, 'loan_id': payment.loan_id, 'amount': payment.amount, 'payment_date': payment.payment_date} for payment in payments]), 200
@app.route('/branches', methods=['GET'])
def get_branches():
    branches = Branch.query.all()
    return jsonify([{'id': branch.id, 'bank_id': branch.bank_id, 'name': branch.name, 'location': branch.location} for branch in branches]), 200
@app.route('/banks/<int:bank_id>', methods=['GET'])
def get_bank(bank_id):
    bank = Bank.query.get_or_404(bank_id)
    return jsonify({'id': bank.id, 'name': bank.name, 'location': bank.location}), 200
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.headers.get('Accept') == 'application/json':
        return jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'phone': user.phone})
    return render_template('user_detail.html', user=user)
@app.route('/accounts/<int:account_id>', methods=['GET'])
def get_account(account_id):
    account = Account.query.get_or_404(account_id)
    return jsonify({'id': account.id, 'user_id': account.user_id, 'account_number': account.account_number, 'balance': account.balance, 'account_type': account.account_type}), 200
@app.route('/transactions/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    return jsonify({'id': transaction.id, 'account_id': transaction.account_id, 'amount': transaction.amount, 'transaction_type': transaction.transaction_type, 'timestamp': transaction.timestamp}), 200
@app.route('/loans/<int:loan_id>', methods=['GET'])
def get_loan(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    return jsonify({'id': loan.id, 'user_id': loan.user_id, 'amount': loan.amount, 'interest_rate': loan.interest_rate, 'status': loan.status}), 200
@app.route('/payments/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    return jsonify({'id': payment.id, 'loan_id': payment.loan_id, 'amount': payment.amount, 'payment_date': payment.payment_date}), 200
@app.route('/branches/<int:branch_id>', methods=['GET'])
def get_branch(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    return jsonify({'id': branch.id, 'bank_id': branch.bank_id, 'name': branch.name, 'location': branch.location}), 200
@app.route('/banks/<int:bank_id>', methods=['DELETE'])
def delete_bank(bank_id):
    bank = Bank.query.get_or_404(bank_id)
    db.session.delete(bank)
    db.session.commit()
    return jsonify({'message': 'Bank deleted successfully!'}), 200
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully!'}), 200
@app.route('/accounts/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    account = Account.query.get_or_404(account_id)
    db.session.delete(account)
    db.session.commit()
    return jsonify({'message': 'Account deleted successfully!'}), 200
@app.route('/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    db.session.delete(transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction deleted successfully!'}), 200
@app.route('/loans/<int:loan_id>', methods=['DELETE'])
def delete_loan(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    db.session.delete(loan)
    db.session.commit()
    return jsonify({'message': 'Loan deleted successfully!'}), 200
@app.route('/payments/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    db.session.delete(payment)
    db.session.commit()
    return jsonify({'message': 'Payment deleted successfully!'}), 200
@app.route('/branches/<int:branch_id>', methods=['DELETE'])
def delete_branch(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    db.session.delete(branch)
    db.session.commit()
    return jsonify({'message': 'Branch deleted successfully!'}), 200
@app.route('/banks/<int:bank_id>', methods=['PUT'])
def update_bank(bank_id):
    data = request.get_json()
    bank = Bank.query.get_or_404(bank_id)
    bank.name = data['name']
    bank.location = data['location']
    db.session.commit()
    return jsonify({'message': 'Bank updated successfully!'}), 200
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get_or_404(user_id)
    user.name = data['name']
    user.email = data['email']
    user.phone = data['phone']
    db.session.commit()
    return jsonify({'message': 'User updated successfully!'}), 200
@app.route('/accounts/<int:account_id>', methods=['PUT'])
def update_account(account_id):
    data = request.get_json()
    account = Account.query.get_or_404(account_id)
    account.user_id = data['user_id']
    account.account_number = data['account_number']
    account.balance = data['balance']
    account.account_type = data['account_type']
    db.session.commit()
    return jsonify({'message': 'Account updated successfully!'}), 200
@app.route('/transactions/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    data = request.get_json()
    transaction = Transaction.query.get_or_404(transaction_id)
    transaction.account_id = data['account_id']
    transaction.amount = data['amount']
    transaction.transaction_type = data['transaction_type']
    db.session.commit()
    return jsonify({'message': 'Transaction updated successfully!'}), 200
@app.route('/loans/<int:loan_id>', methods=['PUT'])
def update_loan(loan_id):
    data = request.get_json()
    loan = Loan.query.get_or_404(loan_id)
    loan.user_id = data['user_id']
    loan.amount = data['amount']
    loan.interest_rate = data['interest_rate']
    loan.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Loan updated successfully!'}), 200      
@app.route('/payments/<int:payment_id>', methods=['PUT'])
def update_payment(payment_id):
    data = request.get_json()
    payment = Payment.query.get_or_404(payment_id)
    payment.loan_id = data['loan_id']
    payment.amount = data['amount']
    payment.payment_date = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Payment updated successfully!'}), 200
@app.route('/branches/<int:branch_id>', methods=['PUT'])
def update_branch(branch_id):
    data = request.get_json()
    branch = Branch.query.get_or_404(branch_id)
    branch.bank_id = data['bank_id']
    branch.name = data['name']
    branch.location = data['location']
    db.session.commit()
    return jsonify({'message': 'Branch updated successfully!'}), 200
@app.route('/')
@login_required
def index():
    user_count = User.query.count()
    account_count = Account.query.count()
    transaction_count = Transaction.query.count()
    loan_count = Loan.query.filter_by(status='active').count()
    
    recent_transactions = Transaction.query.order_by(Transaction.timestamp.desc()).limit(5).all()
    recent_loans = Loan.query.order_by(Loan.id.desc()).limit(5).all()
    
    return render_template('index.html',
                         user_count=user_count,
                         account_count=account_count,
                         transaction_count=transaction_count,
                         loan_count=loan_count,
                         recent_transactions=recent_transactions,
                         recent_loans=recent_loans)

@app.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/accounts')
@login_required
def accounts():
    accounts = Account.query.all()
    users = User.query.all()
    return render_template('accounts.html', accounts=accounts, users=users)

@app.route('/transactions')
@login_required
def transactions():
    transactions = Transaction.query.all()
    return render_template('transactions.html', transactions=transactions)

@app.route('/loans')
@login_required
def loans():
    loans = Loan.query.all()
    return render_template('loans.html', loans=loans)

@app.route('/branches')
@login_required
def branches():
    branches = Branch.query.all()
    return render_template('branches.html', branches=branches)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
