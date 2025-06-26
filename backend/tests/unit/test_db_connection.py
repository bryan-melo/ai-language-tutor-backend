import os
from sqlalchemy import inspect
from app.database.connection import get_database_url, create_engine, create_db_and_tables, get_session

'''
   Positive Test Cases (3)
'''
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
   engine = create_engine(get_database_url())
   create_db_and_tables(engine)
   
   # Inspect tables
   inspector = inspect(engine)
   tables = inspector.get_table_names()
   
   assert "account" in tables


# Test session
def test_get_session(monkeypatch):
   monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
   
   engine = create_engine(get_database_url())
   create_db_and_tables(engine)
   
   session_gen = get_session()
   session = next(session_gen)
   
   inspector = inspect(engine)
   tables = inspector.get_table_names()
   
   # Check that session is returned and account table exists
   assert session is not None
   assert "account" in inspector.get_table_names()
   

'''
   Edge Cases
'''



'''
   Negative Test Cases
'''