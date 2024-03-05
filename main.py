from os import makedirs, path
from uuid import uuid4

from fastapi import FastAPI, HTTPException

from models import Competitor, MatchResult, Tournament
from utils import dump_tournament, load_tournament

app = FastAPI()

@app.get("/")
async def root():
    return {"msg": "Hello World"}

@app.post("/tournament")
async def create_tournament(tournament: Tournament):
    makedirs(".tournaments", exist_ok=True)
    id = uuid4()
    dump_tournament(id, {"id": f"{id}", **tournament.model_dump()})

    return {"id": f"{id}", **tournament.model_dump()}

@app.get("/tournament/{id}")
async def get_tournament(id: str):
    if not path.exists(f".tournaments/{id}.json"):
        raise HTTPException(status_code=404, detail=f"Tournament {id} not found")
    tournament = load_tournament(id)
    
    return tournament

@app.post("/tournament/{id}/competitor")
async def register_competitor(id, competitor: Competitor):
    tournament = load_tournament(id)

    if tournament.get("competitors") is None:
        tournament["competitors"] = []

    competitor_id = uuid4()

    tournament["competitors"].append({
        "id": f"{competitor_id}",
        "name": competitor.name
    })

    dump_tournament(id, tournament)

    return {"id": competitor_id, "name": competitor.name}

@app.get("/tournament/{id}/competitor/{competitor_id}")
async def get_competitor(id, competitor_id: str):
    tournament = load_tournament(id)

    if tournament.get("competitors") is None:
        raise HTTPException(status_code=404, detail="No competitors registered yet")

    return [c for c in tournament["competitors"] if c["id"] == competitor_id][0]

@app.post("/tournament/{id}/match/{match_id}")
async def register_match(id: str, match_id: str, match_result: MatchResult):
    tournament = load_tournament(id)

    match = [c for c in tournament["matches"] if c["id"] == match_id][0]

    competitor_a = [c for c in tournament["competitors"] if c["id"] == match["competitor_a"]][0]
    competitor_b = [c for c in tournament["competitors"] if c["id"] == match["competitor_b"]][0]

    competitor_a["eliminated"] = match_result.competitor_a["eliminated"]
    competitor_b["eliminated"] = match_result.competitor_b["eliminated"]

    dump_tournament(id, tournament)
