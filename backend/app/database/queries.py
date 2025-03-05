from sqlalchemy.orm import Session
from app.database.models import Account

# Create a new account
def create_account(db: Session, account: AccountCreate):
    db_account = Account(
        f_name=account.f_name,
        l_name=account.l_name,
        email=account.email,
        username=account.username,
        password=account.password,
        primary_lang=account.primary_lang
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

# Get account by username
def get_account_by_username(db: Session, username: str):
    return db.query(Account).filter(Account.username == username).first()

# Get account by ID
def get_account_by_id(db: Session, account_id: int):
    return db.query(Account).filter(Account.id == account_id).first()