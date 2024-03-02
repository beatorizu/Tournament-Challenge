from pydantic import BaseModel


class Tournament(BaseModel):
	name: str
