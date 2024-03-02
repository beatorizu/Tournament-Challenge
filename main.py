from json import dump
from os import makedirs
from uuid import uuid4

from fastapi import FastAPI

from models import Tournament

app = FastAPI()

@app.get("/")
async def root():
    return {"msg": "Hello World"}

@app.post("/tournament")
async def create_tournament(tournament: Tournament):
    makedirs(".tournaments", exist_ok=True)
    id = uuid4()
    with open(f".tournaments/{id}.json", "w") as stream:
        dump({"id": f"{id}", **tournament.model_dump()}, stream)
