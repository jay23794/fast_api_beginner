from pydantic import BaseModel

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    username:str or None = None

class User(BaseModel):
    username:str 
    email:str
    full_name:str
    disable:bool

class UserInDB(User):
    hashed_password:str 