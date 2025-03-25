from sqlmodel import Field, SQLModel


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
   

# Login response Schema
class LoginResponse(SQLModel):
   username: str = Field(
      description="Unique username that will be used to log in to the account"
   )
   id: int = Field(
      description="Unique account identifier"
   )
