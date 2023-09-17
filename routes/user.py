from fastapi import APIRouter,Depends, HTTPException,status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from datetime import timedelta
from models.auth import Token,User
from middleware.middleware import ACCESS_TOKEN_EXPIRE_MINUTES, ACCESS_TOKEN_EXPIRE_MINUTES,ALGORITHM, db ,SECRET_KEY,create_access_token,authenticate_user,get_currrent_active_user

user = APIRouter()

       


@user.post("/token",response_model=Token)
async def login_for_access_token(form_data:OAuth2PasswordRequestForm=Depends()):
     user=authenticate_user(db,form_data.username,form_data.password)
     if not user:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, details="incorect username or password",headers={"WWW-Authenticate":"Bearer"})
     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
     access_token=create_access_token(data={"sub":user.username},expires_delta=access_token_expires)
     return {"access_token":access_token,"token_type":"bearer"}   

@user.get("/users/me/",response_model=User)
async def read_users(current_user:User=Depends(get_currrent_active_user)):
    return current_user


@user.get("/users/me/items",response_model=User)
async def read_own_items(current_user:User=Depends(get_currrent_active_user)):
   return JSONResponse([{"item_id":2,'owner':jsonable_encoder(current_user)}])
