from app.database.connection import get_database_url

# Test Database URL
def test_db_url(monkeypatch):
   # Create a fake environment variable
   monkeypatch.setenv("DATABASE_URL", "sqlite://test.db")
   
   db_url = get_database_url()
   assert db_url == "sqlite://test.db"


# Test create database & tables
#def test_create_db_and_tables():
#   pass


## Test session
#def test_get_session():
#   pass


