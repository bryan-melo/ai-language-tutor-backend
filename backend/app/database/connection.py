import os
from sqlmodel import Session, SQLModel, create_engine
from dotenv import load_dotenv
from fastapi import Depends
from typing import Annotated
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import Engine
from typing import Optional

# Load environment variables
load_dotenv()


# Get database URL with a fallback error if not set
def get_database_url():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL is not set. Cannot create database engine")
    return db_url


# Try creating the engine
def safe_create_engine():
    try:
        return create_engine(get_database_url())
    except Exception as e:
        raise RuntimeError(f'Failed to initialize database engine: {e}')


# Import database models
from app.database.schemas import *

def create_db_and_tables(custom_engine: Optional[Engine] = None):
    try:
        SQLModel.metadata.create_all(custom_engine or safe_create_engine())
    except Exception as e:
        raise RuntimeError(f'Failed to create database tables: {e}')


# Get the session
def get_session():
    try:
        with Session(safe_create_engine()) as session:
            yield session
    except SQLAlchemyError as e:
        raise RuntimeError(f"Database session error: {e}")  
    

# Create session dependency
SessionDep = Annotated[Session, Depends(get_session)]
