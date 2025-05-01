import secrets
from fastapi import APIRouter, HTTPException, Cookie, Depends, Response
from typing import Annotated
from sqlmodel import select
from passlib.context import CryptContext
from app.database.connection import SessionDep
from app.database.schemas import Account, AuthToken
from app.models.account_models import AccountRead, LoginRequest
from datetime import datetime, timedelta


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Route to create an account
@router.post("/create/create-account", response_model=AccountRead)
def create_account(account: Account, session: SessionDep) -> AccountRead:
    db_account = Account(**account.dict())
    db_account.password = hash_password(account.password)
    session.add(db_account)
    session.commit()
    session.refresh(db_account)
    return db_account


# Route to get all accounts in database
@router.get("/get-all-accounts", response_model=list[AccountRead])
def get_all_accounts(session: SessionDep) -> list[Account]:
    accounts = session.query(Account).all()

    if not accounts:
        raise HTTPException(status_code=404, detail="No accounts found")

    return accounts


# Route to get an account using account id
@router.get("/get-account/{account_id}", response_model=AccountRead)
def read_account(account_id: int, session: SessionDep) -> AccountRead:
    account = session.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


# Route to delete an existing account
@router.delete("/delete/delete-account/{account_id}")
def delete_account(account_id: int, session: SessionDep):
    account = session.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    session.delete(account)
    session.commit()
    return {"ok": True}


# Route to login
@router.post("/login")
def login(request: LoginRequest, session: SessionDep, response: Response):
    # query for account using username
    account = session.exec(
        select(Account).where(Account.username == request.username)
    ).first()
    
    if not account or not verify_password(request.password, account.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create a new toke
    token = secrets.token_hex(16)    
    auth_token = AuthToken(
        account_id=account.id,
        token=token,
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(days=7)  # Token valid for 7 days
    )
    session.add(auth_token)
    session.commit()
    
    # Set secure cookie
    response.set_cookie(
        key="auth_token",
        value=token,
        httponly=True,
        secure=True,
        samesite='strict',
        max_age=7 * 24 * 60 * 60  # Cookie valid for 7 days
    )

    return {"message": "Login successful"}


# Route to get the current user based on the authentication token
def get_current_user(session: SessionDep, token: str = Cookie(None)) -> AccountRead:
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Lookup token
    auth_token = session.exec(
        select(AuthToken).where(AuthToken.token == token)
    ).first()

    # Check if token exists and hasn't expired
    if not auth_token or auth_token.expires_at < datetime.now(datetime.timezone.utc):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Fetch the account
    account = session.get(Account, auth_token.account_id)
    if not account:
        raise HTTPException(status_code=401, detail="Account not found")

    return account


# Route to log out
@router.post("/logout")
def logout(session: SessionDep, response: Response, token: Annotated[str | None, Cookie()] = None):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Invalidate the token by deleting it from the database
    auth_token = session.exec(
        select(AuthToken).where(AuthToken.token == token)
    ).first()

    if not auth_token:
        raise HTTPException(status_code=401, detail="Invalid token")

    session.delete(auth_token)
    session.commit()

    # Clear the cookie
    response.delete_cookie(
        key="auth_token",
        httponly=True,
        secure=True,
        samesite='strict'
    )

    return {"message": "Logout successful"}
