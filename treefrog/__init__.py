import dis
from pathlib import Path
from typing import Generator

from slippi import Game
from slippi.parse import ParseEvent, parse


def replays(folder_path: str):
    return (str(p) for p in Path(folder_path).rglob("*.slp"))


def games(folder_path: str):
    return (Game(r) for r in replays(folder_path))


def select(gen: Generator): # TODO: Decompile to AST like Pony ORM
    pass


__all__ = ["select"]
