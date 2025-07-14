import pytest
import re

from main import app
from fastapi import HTTPException
from sqlalchemy import inspect
from sqlmodel import select, text
from fastapi.testclient import TestClient
from app.routes.accounts import get_all_accounts
from app.database.connection import safe_create_engine, create_db_and_tables, get_session

client = TestClient(app)


class TestAccountAPI():
   # POSITIVE TEST CASE: Function to test get-all-accounts endpoint
   def test_get_all_accounts_pos(self):
      url = "/account/get-all-accounts"
      response = client.get(url)
         
      # Verify status code
      assert response.status_code == 200
      
      # Verify response structure in accordance with AccountRead pydantic response model
      data = response.json()
      for account in data:
         assert "id" in account
         assert "f_name" in account
         assert "l_name" in account
         assert "email" in account
         assert "username" in account
         assert "primary_lang" in account
         

   # NEGATIVE TEST CASE: Function to test get-all-accounts with no data
   def test_get_all_accounts_no_data_neg(self, monkeypatch):
      monkeypatch.setenv("DATABASE_URL", "sqlite:///./test.db")
      
      # Create a new engine and database
      engine = safe_create_engine()
      create_db_and_tables(engine)
      
      session_gen = get_session()
      session = next(session_gen)
      
      with pytest.raises(HTTPException) as exc_info:
         get_all_accounts(session)
      
      assert exc_info.value.status_code == 404
      assert exc_info.value.detail == "No accounts found"
      
      
         
      
