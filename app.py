# give app.py for models.py 
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, Bank, User, Account, Transaction, Loan, Payment
app = Flask(__name__)   
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()
@app.route('/banks', methods=['POST'])
def create_bank():
    data = request.get_json()
    new_bank = Bank(name=data['name'], location=data['location'])
    db.session.add(new_bank)
    db.session.commit()
    return jsonify({'message': 'Bank created successfully!'}), 201
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'], phone=data['phone'])
    db.session.add(new_user)
    db.session.commit()
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
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'phone': user.phone}), 200
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
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    