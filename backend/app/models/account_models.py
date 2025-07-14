from pydantic import BaseModel


class AccountCreate(BaseModel):
    f_name: str
    l_name: str
    email: str
    username: str
    password: str
    primary_lang: str
    

class AccountRead(BaseModel):
   id: int
   f_name: str
   l_name: str
   email: str
   username: str
   primary_lang: str
   
   
class LoginRequest(BaseModel):
   username: str
   password: str