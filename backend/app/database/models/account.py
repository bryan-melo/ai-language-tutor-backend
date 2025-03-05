from sqlalchemy import Column, Integer, String
from app.database.connection import Base

class Account(Base):
   __tablename__ = "account"
   
   id = Column(Integer, primary_key=True, index=True)
   f_name = Column(String, nullable=False)
   l_name = Column(String, nullable=False)
   email = Column(String, nullable=False, unique=True)
   username = Column(String, nullable=False, unique=True)
   password = Column(String, nullable=False)
   primary_lang = Column(String, nullable=False)