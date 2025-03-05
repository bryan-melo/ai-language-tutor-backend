from pydantic import BaseModel


class AccountBase(BaseModel):
   f_name: str
   l_name: str
   email: str
   username: str
   password: str
   primary_lang: str
   
   
class AccountCreate(AccountBase):
   pass


class Account(AccountBase):
   id: int
   
   class Config:
      orm_mode = True
      
