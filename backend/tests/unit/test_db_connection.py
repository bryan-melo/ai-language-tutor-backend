import os
from sqlmodel import Session
from sqlalchemy import inspect
from app.database.connection import get_database_url, create_engine, create_db_and_tables, get_session


# Test Database URL
def test_db_url(monkeypatch):
   # Create a fake environment variable
   monkeypatch.setenv("DATABASE_URL", "sqlite://test.db")
   
   db_url = get_database_url()
   assert db_url == "sqlite://test.db"


# Test Engine connects to Database URL & database creation
def test_engine(monkeypatch):
   monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
   
   # Create a new engine and database
   engine = create_engine(os.getenv("DATABASE_URL"))
   create_db_and_tables(engine)
   
   # Inspect tables
   inspector = inspect(engine)
   tables = inspector.get_table_names()
   assert "account" in tables


# Test session
def test_get_session():
   pass
