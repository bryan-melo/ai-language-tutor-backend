from app.models.course_models import SupportedLanguages

from sqlmodel import Field, SQLModel, Column, Enum as SqlEnum
from typing import Optional


# Account Creation Schema
class Account(SQLModel, table=True):   
   id: Optional[int] = Field(
      default=None, 
      primary_key=True, 
      index=True,
      description="Unique account identifier"
   )
   f_name: str = Field(
      description="First name of account creator"
   )
   l_name: str = Field(
      description="Last name of account creator"
   )
   email: str = Field(
      unique=True,
      description="Unique email associated with account"
   )
   username: str = Field(
      unique=True,
      description="Unique username that will be used to log in to the account"   
   )
   password: str = Field(
      description="Password for account that will be used for login"
   )
   primary_lang: SupportedLanguages = Field(
        sa_column=Column(SqlEnum(SupportedLanguages)),
        description="Primary language used for translation"
    )