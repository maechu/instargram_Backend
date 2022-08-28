from typing import List, Union,Optional
from fastapi import UploadFile,Form
from pydantic import BaseModel
from datetime import datetime
   
class UserRegister(BaseModel):
    user_id:str
    nickname:str
    password:str
    profile_image: Optional[str]=None
    class Config:
        orm_mode = True
        

class IdCheck(BaseModel):
    user_id:str
    class Config:
        orm_mode = True


class NicksCheck(BaseModel):
    nickname:str
    class Config:
        orm_mode = True


class Login(BaseModel):
    user_id:str
    password:str
    class Config:
        orm_mode = True