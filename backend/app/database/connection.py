import os
from sqlmodel import Session, SQLModel, create_engine
from dotenv import load_dotenv
from fastapi import Depends
from typing import Annotated

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine
connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, connect_args=connect_args)


# Create Database & tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Get the session
def get_session():
    with Session(engine) as session:
        yield session


# Create session dependency 
SessionDep = Annotated[Session, Depends(get_session)]
