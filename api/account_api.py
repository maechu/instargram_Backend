from sqlalchemy.orm import Session
from fastapi import  Depends,APIRouter
from home.auth import AuthHandler
from home import schemas as home_schemas
from home import models as home_models
from datetime import datetime
from fastapi.responses import JSONResponse
import bcrypt
from typing import List, Union,Optional
import time
from home.database import home_db
import json

router = APIRouter()

#  데이터베이스는 Pydantic model을 받지 않고 dict만 받는 경우가 있다.
# 또는 datetime을 데이터베이스로 넘겨줄때 str로 바꿔주어야 한다.
# 이럴때 jsonable_encoder를 사용한다.
auth_handler = AuthHandler()


@router.post('/register',tags=["account"])
def register(data: home_schemas.UserRegister,home_db:Session=Depends(home_db)):
    
    user_id = data.user_id
    password = data.password
    nickname = data.nickname
    profile_image = data.profile_image

    #만약에 데이터베이스 안에 , 똑같은 user_id 가 이미 존재한다면?
    #종료시킨다. + 프론트에 오류를 전달해야해요.
    if home_db.query(home_models.User)\
        .filter(home_models.User.user_id == user_id ).first() != None:

        return JSONResponse({'error':'user_id already exists'},status_code = 401)

    password = bcrypt.hashpw(password.encode(encoding='utf-8'),bcrypt.gensalt()).decode('utf-8')
    
    if profile_image == None:
        user = home_models.User(user_id = user_id,
        password = password,
        nickname = nickname)
    else:
        user = home_models.User(user_id = user_id,
        password = password,
        nickname = nickname,
        profile_image = profile_image)
    
    home_db.add(user)
    home_db.commit()

    return JSONResponse({'message':'register success'},status_code = 201)
    

        #데이터가 100개여도 가장 첫번재 데이터는 존재해요
        #데이터가 1개여도 가장 첫번째 데이터는 존재해요
        #단, 데이터가 0개이면 가장 첫번째 데이터는 없어요.
    

