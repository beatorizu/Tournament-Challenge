from json import dump, load


def dump_tournament(id: str, tournament: dict):
    with open(f".tournaments/{id}.json", "w") as stream:
        dump(tournament, stream)


def load_tournament(id: str):
    with open(f".tournaments/{id}.json") as stream:
        return load(stream)