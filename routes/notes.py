from fastapi import APIRouter,FastAPI, Request
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
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id":doc['_id'],
            "title":doc['title'],
            "desc":doc['desc'],
            "important":doc['important'],
        })
    return templates.TemplateResponse("index.html",{"request":request,"newDocs":newDocs})

@note.post("/add_node") 
async def add_node(request:Request):
    form = await request.body()
    encodedData = json.loads(form)
    conn.notes.notes.insert_one(dict(encodedData))

    return {'success':True}