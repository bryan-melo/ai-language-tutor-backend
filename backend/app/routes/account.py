from fastapi import APIRouter, HTTPException
from typing import Annotated
from sqlmodel import select
from app.database.connection import SessionDep
from app.database.models import Account

router = APIRouter()

# Route to create an account
@router.post("/")
def create_account_route(account: Account, session: SessionDep) -> Account:
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


# Route to get an account using account id
@router.get("/get-account/{account_id}")
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
@router.post("/login")
def login(username: str, password: str, session: SessionDep) -> dict:
    # query for account using username
    statement = select(Account).where(Account.username == username).where(Account.password == password) # query the database to find an account that matches the username
    account = session.exec(statement).first() # executes the query and retrieves the first result
    
    if not account:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    return {"username": account.username, "id": account.id}
    