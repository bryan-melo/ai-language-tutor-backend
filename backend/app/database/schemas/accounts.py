from sqlmodel import Field, SQLModel
from datetime import datetime, timedelta


# Account Creation Schema
class Account(SQLModel, table=True):   
   id: int | None = Field(
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
   primary_lang: str = Field(
      description="Primary language used for default language to translate to"
   )
   
   
class AccountRead(SQLModel):
   id: int
   f_name: str
   l_name: str
   email: str
   username: str
   primary_lang: str
   

class AuthToken(SQLModel, table=True):
   id: int | None = Field(
      default=None,
      primary_key=True,
      description="Unique identifier for the authentication token"
   )
   account_id: int = Field(
      foreign_key="account.id",
      description="ID of the account associated with this token"
   )
   token: str = Field(
      unique=True,
      index=True,
      description="Authentication token string"
   )
   created_at: datetime = Field(
      default_factory=datetime.utcnow,
      description="Timestamp when the token was created"
   )
   expires_at: datetime = Field(
      default_factory=lambda: datetime.now(datetime.timezone.utc) + timedelta(days=7), 
      description="Timestamp when the token expires"
    )