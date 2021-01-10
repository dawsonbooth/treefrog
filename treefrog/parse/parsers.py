from __future__ import annotations

import calendar
from datetime import timezone

from slippi import Game

from .utils import character_name, characters, stage_name


def matchup(game: Game) -> str:
    c1, c2 = tuple(characters(game))
    return f"{character_name(c1)} vs {character_name(c2)}"


def stage(game: Game) -> str:
    return stage_name(game.start.stage)


def timestamp(game: Game) -> str:
    utc_dt = game.metadata.date
    dt = utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
    return f"{dt.year}{dt.month:02}{dt.day:02}T{dt.hour:02}{dt.minute:02}{dt.second:02}"


def year(game: Game) -> str:
    return str(game.metadata.date.year)


def month(game: Game) -> str:
    return calendar.month_name[game.metadata.date.month]


def day(game: Game) -> str:
    return str(game.metadata.date.day)


def hour(game: Game) -> str:
    return str(game.metadata.date.hour)


def minute(game: Game) -> str:
    return str(game.metadata.date.minute)


def second(game: Game) -> str:
    return str(game.metadata.date.second)


__all__ = "matchup", "stage", "timestamp", "year", "month", "day", "hour", "minute", "second"
