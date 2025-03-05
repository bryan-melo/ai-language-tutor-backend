from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.schemas.account import AccountCreate, Account
from app.database.queries import create_account as create_account_db, get_account_by_username, get_account_by_id
from app.database.connection import get_db

router = APIRouter()


@router.post("/account", response_model=Account)
def create_account_route(account: AccountCreate, db: Session = Depends(get_db)):
    db_account = get_account_by_username(db, account.username)  # Use the function directly
    if db_account:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_account_db(db=db, account=account)  # Use the function directly


@router.get("/account/{account_id}", response_model=Account)
def read_account(account_id: int, db: Session = Depends(get_db)):
    db_account = get_account_by_id(db, account_id)  # Use the function directly
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account