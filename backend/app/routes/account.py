from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import AccountCreate, Account
from app.database.queries import *
from app.database.connection import get_db

router = APIRouter()


@router.post("/account", response_model=Account)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    db_account = queries.get_account_by_username(db, account.username)
    if db_account:
        raise HTTPException(status_code=400, detail="Username already registered")
    return queries.create_account(db=db, account=account)


@router.get("/account/{account_id}", response_model=Account)
def read_account(account_id: int, db: Session = Depends(get_db)):
    db_account = queries.get_account_by_id(db, account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account
 