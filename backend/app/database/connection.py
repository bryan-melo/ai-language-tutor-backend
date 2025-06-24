import os
from sqlmodel import Session, SQLModel, create_engine
from dotenv import load_dotenv
from fastapi import Depends
from typing import Annotated

# Load environment variables
load_dotenv()


def get_database_url():
    return os.getenv("DATABASE_URL")

# Create engine
engine = create_engine(get_database_url())

# Import database models
from app.database.schemas import *


# Create Database & tables
def create_db_and_tables(custom_engine=None):
    SQLModel.metadata.create_all(custom_engine or engine)


# Get the session
def get_session():
    with Session(engine) as session:
        yield session


# Create session dependency 
SessionDep = Annotated[Session, Depends(get_session)]
