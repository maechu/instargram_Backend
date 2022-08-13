from fastapi import  Depends,APIRouter
from home.auth import AuthHandler
from fastapi.responses import JSONResponse

router = APIRouter()
auth_handler = AuthHandler()



@router.get('/')
def test():
    print('test')
    return JSONResponse({'message':'test'})

##http://localhost:8000/test