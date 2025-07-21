from pydantic import BaseModel, ConfigDict


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
   
   model_config = ConfigDict(from_attributes=True)
   
   
class LoginRequest(BaseModel):
   username: str
   password: str
   