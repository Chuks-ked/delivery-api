from pydantic import BaseModel
from typing import Optional

class SignupModel(BaseModel):
    id:Optional[int]
    username:str
    email:str
    password:str
    is_staff:Optional[bool]
    is_active:Optional[bool]

    class Config:
        orm_mode=True
        schema_extra={
            'example':{
                "username":"johndoe",
                "email":"johndoe@gmail.com",
                "password":"passwprd",
                "is_staff":False,
                "is_active":True
            }
        }


class Settings(BaseModel):
    authjwt_key:str='2233c7af0d6a75acf09b0e3175455e677b4181eadaa32184ac51540782e5936e'

class LoginModel(BaseModel):
    username:str
    password:str