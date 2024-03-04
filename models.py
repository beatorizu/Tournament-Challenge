from pydantic import BaseModel


class Tournament(BaseModel):
	name: str


class Competitor(BaseModel):
	name:str


class MatchResult(BaseModel):
	competitor_a: dict
	competitor_b: dict
