from bson import ObjectId
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from models.note import Note
from config.db import conn
from schema.note import noteEntity,notesEntity
from fastapi.templating import Jinja2Templates
import json

note = APIRouter()


templates = Jinja2Templates(directory="templates")

@note.get("/",response_class=HTMLResponse  )
def read_root(request:Request):
    docs = conn.notes.notes.find({})
    newDocs:Note=[]
    for doc in docs:
        newDocs.append({
            "id":doc['_id'],
            "title":doc['title'],
            "desc":doc['desc'],
            "important":doc['important'],
        })
    return templates.TemplateResponse("index.html",{"request":request,"newDocs":newDocs})

@note.get("/get_note") 
async def get_note(request:Request):
    docs = conn.notes.notes.find({})
    newDocs:Note=[]
    
    for doc in docs:
        newDocs.append({
            "id":str(doc['_id']),
            "title":doc['title'],
            "desc":doc['desc'],
            "important":doc['important'],
        })
    return {'success':True,'message':"added successfuly","newDocs":newDocs}



@note.post("/add_note") 
async def add_note(request:Request):
    form = await request.body()
    encodedData = json.loads(form)
    conn.notes.notes.insert_one(dict(encodedData))
    return {'success':True,'message':"added successfuly"}

@note.delete("/delete_note") 
async def delete_note(request:Request):
    requestData = await request.body()
    encodedData = json.loads(requestData)
    conn.notes.notes.delete_one({ "_id" :ObjectId(encodedData['id']) })
    return {'success':True,'message':"deleted successfuly"}

@note.put("/update_note") 
async def update_note(request:Request):
    requestData = await request.body()
    encodedData = json.loads(requestData)
    conn.notes.notes.update_one({"_id" :ObjectId(encodedData['id'])},{"$set":{'title':encodedData['title'],'desc':encodedData['desc'],'important':encodedData['important']}})
    return {'success':True,'message':"updated successfuly"}

@note.get("/test/{test_id}/")
async def test_note(test_id:str,query:int=1):
     return {'success':True,'message':"Tested successfuly"}