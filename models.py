from pydantic import BaseModel


class Tournament(BaseModel):
	name: str


class Competitor(BaseModel):
	name:str
