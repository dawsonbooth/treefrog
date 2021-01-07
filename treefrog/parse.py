from __future__ import annotations

import calendar
from datetime import datetime
from typing import Any, Callable, Tuple

from slippi import Game
from slippi.id import InGameCharacter
from slippi.id import Stage as _Stage

from treefrog.format import character_name, stage_name, timestamp


class ParseError(Exception):
    pass


class Parser:
    __slots__ = "store",

    store: Any

    parse: Callable[[Game], None]

    def __init__(self, game: Game, **kwargs):
        try:
            self.parse(game, **kwargs)
        except AttributeError:
            raise ParseError

    def __str__(self):
        return str(self.store)


class NetplayName(Parser):
    def parse(self, game: Game, netplay_code: str, **kwargs):
        for player in game.metadata.players:
            if player and player.netplay.code == netplay_code:
                self.store: str = player.netplay.name


class NetplayCode(Parser):
    def parse(self, game: Game, netplay_code: str, **kwargs):
        for player in game.metadata.players:
            if player and player.netplay.code == netplay_code:
                self.store: str = player.netplay.code


class OpponentNetplayName(Parser):
    def parse(self, game: Game, netplay_code: str, **kwargs):
        for player in game.metadata.players:
            if player and player.netplay.code != netplay_code:
                self.store: str = player.netplay.name


class OpponentNetplayCode(Parser):
    def parse(self, game: Game, netplay_code: str, **kwargs):
        for player in game.metadata.players:
            if player and player.netplay.code != netplay_code:
                self.store: str = player.netplay.code


class Character(Parser):
    def parse(self, game: Game, netplay_code: str, **kwargs):
        for player in game.metadata.players:
            if player and player.netplay.code == netplay_code:
                self.store: InGameCharacter = sorted(
                    player.characters.keys(),
                    key=lambda c: player.characters[c]
                )[0]

    def __str__(self) -> str:
        return character_name(self.store)


class OpponentCharacter(Parser):
    def parse(self, game: Game, netplay_code: str, **kwargs):
        for player in game.metadata.players:
            if player and player.netplay.code != netplay_code:
                self.store: InGameCharacter = sorted(
                    player.characters.keys(),
                    key=lambda c: player.characters[c]
                )[0]

    def __str__(self) -> str:
        return character_name(self.store)


class Matchup(Parser):
    def parse(self, game: Game, netplay_code: str, **kwargs):
        character = Character(
            game, netplay_code=netplay_code
        ).store
        opponent_character = OpponentCharacter(
            game, netplay_code=netplay_code
        ).store

        self.store: Tuple[InGameCharacter] = (character, opponent_character)

    def __str__(self) -> str:
        return " vs ".join(character_name(c) for c in self.store)


class Stage(Parser):
    def parse(self, game: Game, **kwargs):
        self.store: _Stage = game.start.stage

    def __str__(self) -> str:
        return stage_name(self.store)


class DateTime(Parser):
    def parse(self, game: Game, **kwargs):
        self.store: datetime = game.metadata.date

    def __str__(self) -> str:
        return timestamp(self.store)


class Year(Parser):
    def parse(self, game: Game, **kwargs):
        self.store: int = DateTime(game).store.year


class Month(Parser):
    def parse(self, game: Game, **kwargs):
        self.store: int = DateTime(game).store.month

    def __str__(self):
        return calendar.month_name[self.store]


class Day(Parser):
    def parse(self, game: Game, **kwargs):
        self.store: int = DateTime(game).store.day


class Hour(Parser):
    def parse(self, game: Game, **kwargs):
        self.store: int = DateTime(game).store.hour


class Minute(Parser):
    def parse(self, game: Game, **kwargs):
        self.store: int = DateTime(game).store.minute


class Second(Parser):
    def parse(self, game: Game, **kwargs):
        self.store: int = DateTime(game).store.second
