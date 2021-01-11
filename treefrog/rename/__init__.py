from slippi import Game
from slippi.parse import ParseError

from ..parse.parsers import stage, timestamp
from ..parse.utils import character_name, characters


def default_filename(game: Game) -> str:
    return f"Game_{timestamp(game)}.slp"


def create_filename(game: Game) -> str:
    try:
        p1, p2 = tuple(characters(game))
        return f"{timestamp(game)} - {character_name(p1)} vs {character_name(p2)} - {stage(game)}.slp"
    except ParseError:
        return default_filename(game)
