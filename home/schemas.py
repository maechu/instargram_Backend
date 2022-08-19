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
        