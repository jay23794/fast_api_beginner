# from typing import Union

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

conn=MongoClient("mongodb+srv://jayprmr27:bRdigpajJnvPoZov@cluster0.yl1ojdw.mongodb.net")

@app.get("/",response_class=HTMLResponse  )
def read_root(request:Request):
    docs = conn.notes.notes.find({})
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id":doc['_id'],
            "note":doc['note']
        })
    return templates.TemplateResponse("index.html",{"request":request,"newDocs":newDocs})







