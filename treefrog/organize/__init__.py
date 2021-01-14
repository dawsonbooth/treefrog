from pathlib import Path
from typing import Sequence

from slippi.game import Game

from ..parse import Parser
from ..parse.parsers import matchup, month, stage, year
from ..parse.utils import ParseError

Ordering = Sequence[Parser]

default_ordering = (year, month, matchup, stage)


def build_parent(game: Game, ordering: Ordering = default_ordering) -> Path:
    try:
        parent = Path()

        for parser in ordering:
            parent /= str(parser(game))

        return parent
    except ParseError:
        return Path("Error")
