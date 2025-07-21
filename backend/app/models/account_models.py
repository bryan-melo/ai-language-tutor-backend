from pydantic import BaseModel, ConfigDict
from app.models.course_models import SupportedLanguages


class AccountCreate(BaseModel):
    f_name: str
    l_name: str
    email: str
    username: str
    password: str
    primary_lang: SupportedLanguages
    
    model_config = ConfigDict(from_attributes=True)
    

class AccountRead(BaseModel):
   id: int
   f_name: str
   l_name: str
   email: str
   username: str
   primary_lang: SupportedLanguages
   
   model_config = ConfigDict(from_attributes=True)
   
   
class LoginRequest(BaseModel):
   username: str
   password: str
   