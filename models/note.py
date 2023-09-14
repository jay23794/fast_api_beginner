from pydantic import BaseModel

class Note(BaseModel):
    id:str
    title:str
    desc:str
    important:bool