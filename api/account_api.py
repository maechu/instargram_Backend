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
    

@router.post('/id/check',tags=["account"])
def id_check(data:home_schemas.IdCheck ,home_db:Session=Depends(home_db)):
    try:
        id = home_db.query(home_models.User).filter(home_models.User.user_id == data.user_id).first()
        
        if id != None:
            return JSONResponse({'Error':"Id already exists"},status_code=400)
        
        else:
            return JSONResponse({'Message':"Id can use"},status_code=200)
    except Exception as e:
        return e


@router.post('/nick/check',tags=["account"])
def nick_check(data:home_schemas.NicksCheck ,home_db:Session=Depends(home_db)):
    try:
        nick_name = home_db.query(home_models.User).filter(home_models.User.nickname == data.nickname).first()
        
        if nick_name != None:
            return JSONResponse({'Error':"nick_name already exists"},status_code=400)
        
        else:
            return JSONResponse({'Message':"nick_name can use"},status_code=200)
    except Exception as e:
        return e


@router.post('/login',tags=["account"])
def login(data:home_schemas.Login ,home_db:Session=Depends(home_db)):
    try:
        user = home_db.query(home_models.User).filter(home_models.User.user_id == data.user_id).one()
        print(data.password)
        if not bcrypt.checkpw(data.password.encode('utf-8'), user.password.encode('utf-8')):
            return JSONResponse({"error":"비번 미존재"},status_code=401) # 비밀번호 오류


        token = auth_handler.encode_token(user.user_id)

        print('로그인 성공')
    
        return JSONResponse({'token': token})
    except Exception as e:
        print(e)
        return JSONResponse({"error":"유저 미존재"},status_code=400) # 아이디 오류
