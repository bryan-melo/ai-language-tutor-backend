from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from passlib.context import CryptContext
from app.database.connection import SessionDep
from app.database.schemas import Account
from app.models.account_models import AccountRead, LoginRequest, AccountCreate

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Route to create an account
@router.post("/create/create-account", response_model=AccountRead, status_code=status.HTTP_201_CREATED)
def create_account(account: AccountCreate, session: SessionDep) -> AccountRead:
    db_account = Account(**account.model_dump())
    db_account.password = hash_password(account.password)
    session.add(db_account)
    session.commit()
    session.refresh(db_account)
    return db_account


# Route to login
@router.post("/login", response_model=AccountRead, status_code=status.HTTP_200_OK)
def login(request: LoginRequest, session: SessionDep) -> AccountRead:
    account = session.exec(
        select(Account).where(Account.username == request.username)
    ).first()
    if not account or not verify_password(request.password, account.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return account


# Route to get all accounts in database
@router.get("/get-all-accounts", response_model=list[AccountRead], status_code=status.HTTP_200_OK)
def get_all_accounts(session: SessionDep) -> list[Account]:
    accounts = session.exec(
        select(Account)
    )
    if accounts.all() is None:
        return []
    return accounts


# Route to get an account using account id
@router.get("/get-account/{account_id}", response_model=AccountRead)
def get_account(account_id: int, session: SessionDep) -> AccountRead:
    account = session.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


# Route to delete an existing account
@router.delete("/delete/delete-account/{account_id}", status_code=status.HTTP_200_OK)
def delete_account(account_id: int, session: SessionDep):
    account = session.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    session.delete(account)
    session.commit()
    return {"ok": True}


# Route to log out
@router.post("/logout")
def logout(session: SessionDep):
    pass
