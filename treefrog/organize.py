from pathlib import Path
from typing import Sequence

from slippi.game import Game

from .parse import Matchup, Month, OpponentNetplayCode, ParseError, Parser, Stage, Year

Ordering = Sequence[Parser]


default_ordering = (
    Year,
    Month,
    OpponentNetplayCode,
    Matchup,
    Stage
)


def organized_path(source: str, netplay_code: str, ordering: Ordering = default_ordering):
    path = Path()

    game = Game(source)

    for parser in ordering:
        game_attribute = parser(game, netplay_code=netplay_code)
        path /= str(game_attribute)

    return path / Path(source).name
