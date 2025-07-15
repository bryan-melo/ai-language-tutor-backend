import pytest
from sqlalchemy import inspect
from app.database.connection import get_database_url, safe_create_engine, create_db_and_tables, get_session


class TestDatabaseConnection:
   # Test Database URL with a valid env. variable for Database
   def test_db_url_pos(self, monkeypatch):
      monkeypatch.setenv("DATABASE_URL", "sqlite://test.db")
      db_url = get_database_url()
      
      assert db_url == "sqlite://test.db"


   # Test Database URL without an env. variable for Database
   def test_db_url_neg(self, monkeypatch):
      monkeypatch.delenv("DATABASE_URL", raising=False)
      
      with pytest.raises(RuntimeError) as exc_info:
         get_database_url()
         
      assert str(exc_info.value) == "DATABASE_URL is not set. Cannot create database engine"


   # Test Engine connects to Database URL & database creation
   def test_engine_pos(self, monkeypatch):
      monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
      
      # Create a new engine and database
      engine = safe_create_engine()
      create_db_and_tables(engine)
      
      # Inspect tables
      inspector = inspect(engine)
      tables = inspector.get_table_names()
      
      assert "account" in tables


   # Test Engine failure to connect to Database URL with invalid URL
   def test_engine_neg(self, monkeypatch):
      monkeypatch.setenv("DATABASE_URL", "")
      
      with pytest.raises(RuntimeError) as exc_info:
         _ = safe_create_engine()
         
      assert "Failed to initialize database engine" in str(exc_info.value)


   # Test session with a valid engine 
   def test_get_session_pos(self, monkeypatch):
      monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
      
      engine = safe_create_engine()
      create_db_and_tables(engine)
      
      session_gen = get_session()
      session = next(session_gen)
      
      inspector = inspect(engine)
      tables = inspector.get_table_names()
      
      # Check that session is returned and account table exists
      assert session is not None
      assert "account" in tables
      
      
   # Test session with invalid engine
   def test_get_session_neg(self, monkeypatch):
      monkeypatch.setenv("DATABASE_URL", "")
      
      with pytest.raises(RuntimeError) as exc_info:
         session_gen = get_session()
         next(session_gen)
         
      assert "DATABASE_URL is not set" in str(exc_info.value)
