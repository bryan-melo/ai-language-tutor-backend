from fastapi import APIRouter, HTTPException
from typing import Annotated
from app.database.connection import SessionDep
from app.database.models import Account

router = APIRouter()


@router.post("/account/")
def create_account_route(account: Account, session: SessionDep) -> Account:
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


@router.get("/account/{account_id}")
def read_account(account_id: int, session: SessionDep) -> Account:
    account = session.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.delete("/account/{account_id}")
def delete_account(account_id: int, session: SessionDep):
    account = Session.get(Account, account_id)
    if not accout:
        raise HTTPException(status_code=404, detail="Account not found")
    session.delete(account)
    session.commit()
    return {"ok": True}