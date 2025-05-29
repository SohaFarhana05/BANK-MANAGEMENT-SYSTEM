# database for bank management system 
# use SQLAlchemy for database operations - make classes for each table that are bank,user,account,transaction,loan,payment,branch,atm,bank_staff

# keep it basic and simple, no complex relationships or constraints
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Base = declarative_base()
# Bank model
class Bank(Base):
    __tablename__ = 'banks'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    established_date = Column(DateTime, nullable=False)
    def __repr__(self):
        return f"<Bank(name={self.name}, location={self.location})>"
# User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)
    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"
# Account model     
class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    account_number = Column(String, unique=True, nullable=False)
    balance = Column(Float, default=0.0)
    account_type = Column(String, nullable=False)  # e.g., savings, checking
    def __repr__(self):
        return f"<Account(account_number={self.account_number}, balance={self.balance})>"
# Transaction model
class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)  # e.g., deposit, withdrawal
    timestamp = Column(DateTime, nullable=False)
    def __repr__(self):
        return f"<Transaction(amount={self.amount}, type={self.transaction_type})>"
# Loan model
class Loan(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    status = Column(String, nullable=False)  # e.g., approved, pending, rejected
    def __repr__(self):
        return f"<Loan(amount={self.amount}, status={self.status})>"
# Payment model
class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    loan_id = Column(Integer, ForeignKey('loans.id'), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, nullable=False)
    def __repr__(self):
        return f"<Payment(amount={self.amount}, date={self.payment_date})>"
# Branch model
class Branch(Base):
    __tablename__ = 'branches'
    id = Column(Integer, primary_key=True)
    bank_id = Column(Integer, ForeignKey('banks.id'), nullable=False)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    def __repr__(self):
        return f"<Branch(name={self.name}, location={self.location})>"
# ATM model 
class ATM(Base):
    __tablename__ = 'atms'
    id = Column(Integer, primary_key=True)
    branch_id = Column(Integer, ForeignKey('branches.id'), nullable=False)
    atm_number = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=False)
    def __repr__(self):
        return f"<ATM(atm_number={self.atm_number}, location={self.location})>"
# Bank Staff model
class BankStaff(Base):
    __tablename__ = 'bank_staff'
    id = Column(Integer, primary_key=True)
    bank_id = Column(Integer, ForeignKey('banks.id'), nullable=False)
    name = Column(String, nullable=False)
    position = Column(String, nullable=False)  # e.g., teller, manager
    def __repr__(self):
        return f"<BankStaff(name={self.name}, position={self.position})>"
# Database setup
DATABASE_URL = 'sqlite:///bank_management_system.db'  # Use SQLite for simplicity
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
def get_session():
    return Session()
# Function to get a new session
def create_session():
    session = get_session()
    return session
# Function to close the session
def close_session(session):
    session.close()
# Function to drop all tables (for testing purposes)
def drop_all_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)  # Recreate tables after dropping
# Uncomment the following line to drop all tables and recreate them
# drop_all_tables()
# Example usage
if __name__ == "__main__":
    session = create_session()
    # Example: Add a new bank
    new_bank = Bank(name="Example Bank", location="New York", established_date="2023-01-01")
    session.add(new_bank)
    session.commit()
    print("Bank added:", new_bank)
    close_session(session)
# Example: Add a new user
# new_user = User(name="John Doe", email="john.doe@example.com", phone="123-456-7890", address="123 Elm St")
# session.add(new_user)
# session.commit()
# print("User added:", new_user)
# close_session(session)
# Example: Add a new account
# new_account = Account(user_id=1, account_number="123456789", balance=1000.0, account_type="savings")
# session.add(new_account)
# session.commit()
# print("Account added:", new_account)
# close_session(session)
# Example: Add a new transaction
# new_transaction = Transaction(account_id=1, amount=200.0, transaction_type="deposit", timestamp="2023-01-02 10:00:00")