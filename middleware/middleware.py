from fastapi import APIRouter,Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from models.auth import TokenData,UserInDB
from jose.exceptions import JWTError
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime,timedelta
SECRET_KEY='cebe08f33d415029aee94e635ef5e889a4f751d935f9c7a9ea5acece757d3aea'
ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Authenticate user check wether the user is present or not
# Create access token
# Check access token  for every API

db = {
    "jay":{
        "username":"jay",
        "full_name":"jay parmar",
        "email":"jay@gmail.com",
        "hashed_password":"$2b$12$D4KhQgbvfBrW778sbErlCe3OYKkSQ5BclqjxqbPn1u2.XulLHoa.e",
        "disable":False
    }
}
pwd_context = CryptContext(schemes=["bcrypt"],deprecated='auto')
oauth_2_scheme =  OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_passsword,hashed_password):
    return pwd_context.verify(plain_passsword,hashed_password )

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db,username:str):
   if username in db:
        user_data = db[username]
        return UserInDB(**user_data)

def create_access_token(data:dict,expires_delta:timedelta or None = None):
     to_encode = data.copy()
     if expires_delta:
        expires = datetime.utcnow() + expires_delta
     else:
        expires = datetime.utcnow() +timedelta(minutes=15)
    
     to_encode.update({"exp":expires}) 
     encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
     return encoded_jwt       

async def get_curret_user(token:str = Depends(oauth_2_scheme)):
    credemtial_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate credential",headers={"WWW-Authenticate":"Bearer"})

    try:
        payload =jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str =payload.get("sub")
        if username is None:
            raise credemtial_exception
        
        token_data = TokenData(username=username)
    except JWTError:    
        raise credemtial_exception
    
    user = get_user(db,username=token_data.username)
    if user is None:
         raise credemtial_exception
    
    return user

async def get_currrent_active_user(current_user:UserInDB=Depends(get_curret_user)):
    if current_user.disable:
        raise HTTPException(status_code=400,detail="Inactive user")
    return current_user

def authenticate_user(db,username:str,password:str):
    user = get_user(db,username)
    if not user:
        return False
    if not verify_password(password,user.hashed_password):
        return False
    return user  
