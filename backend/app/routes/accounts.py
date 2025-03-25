from fastapi import APIRouter, HTTPException
from typing import Annotated
from sqlmodel import select
from app.database.connection import SessionDep
from app.database.schemas import Account, LoginResponse

router = APIRouter()


# Route to create an account
@router.post("/create-account", response_model=Account)
def create_account(account: Account, session: SessionDep) -> Account:
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


# Route to get all accounts in database
@router.post("/get-all-accounts", response_model=list[Account])
def get_all_accounts(session: SessionDep) -> list[Account]:
    accounts = session.query(Account).all()

    if not accounts:
        raise HTTPException(status_code=404, detail="No accounts found")

    return accounts


# Route to get an account using account id
@router.get("/get-account/{account_id}", response_model=Account)
def read_account(account_id: int, session: SessionDep) -> Account:
    account = session.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


# Route to delete an existing account
@router.delete("/delete-account/{account_id}")
def delete_account(account_id: int, session: SessionDep):
    account = session.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    session.delete(account)
    session.commit()
    return {"ok": True}


# Route to login
@router.post("/login", response_model=LoginResponse)
def login(username: str, password: str, session: SessionDep) -> LoginResponse:
    # query for account using username
    statement = select(Account).where(Account.username == username).where(Account.password == password) # query the database to find an account that matches the username
    account = session.exec(statement).first() # executes the query and retrieves the first result
    
    if not account:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    return LoginResponse(username=account.username, id=account.id)
    