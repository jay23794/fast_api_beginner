from fastapi import FastAPI, Request
from routes.notes import note
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(note)    