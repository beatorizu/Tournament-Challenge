from json import dump, load
from os import makedirs, path
from uuid import uuid4

from fastapi import FastAPI, HTTPException

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

@app.get("/tournament/{id}")
async def get_tournament(id: str):
    if not path.exists(f".tournaments/{id}.json"):
        raise HTTPException(status_code=404, detail=f"Tournament {id} not found")
    with open(f".tournaments/{id}.json") as stream:
        tournament = load(stream)
    
    return tournament
