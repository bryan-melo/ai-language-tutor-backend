from sqlmodel import Field, SQLModel

class Account(SQLModel, table=True):   
   id: int | None = Field(default=None, primary_key=True, index=True)
   f_name: str
   l_name: str
   email: str = Field(unique=True)
   username: str = Field(unique=True)
   password: str
   primary_lang: str