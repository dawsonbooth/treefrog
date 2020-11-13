from enum import Enum
from typing import Any, Dict, Iterable, Union

from slippi.event import Start
from slippi.metadata import Metadata
from slippi.parse import ParseEvent, parse


class Hierarchy():
    class Level(Enum):
        STAGE = 0
        NAME = 1
        CODE = 2
        CHARACTER = 3
        OPPONENT_NAME = 5
        OPPONENT_CODE = 6
        OPPONENT_CHARACTER = 7

    class Ordering (Iterable[Union[Level, Iterable[Level]]]):
        pass


def get_members(game_path: str, netplay_code: str) -> Dict[Hierarchy.Level, Any]:
    attributes = {
        Hierarchy.Level.CODE: netplay_code
    }

    def parse_start(start: Start):
        attributes[Hierarchy.Level.STAGE] = start.stage

    def parse_metadata(metadata: Metadata):
        for player in metadata.players:
            if player is not None:
                code = player.netplay.code
                name = player.netplay.name
                character = sorted(
                    player.characters.keys(),
                    key=lambda c: player.characters[c]
                )[0]
                if code == netplay_code:
                    attributes[Hierarchy.Level.NAME] = name
                    attributes[Hierarchy.Level.CHARACTER] = character
                else:
                    attributes[Hierarchy.Level.OPPONENT_CODE] = code
                    attributes[Hierarchy.Level.OPPONENT_NAME] = name
                    attributes[Hierarchy.Level.OPPONENT_CHARACTER] = character

    handlers = {
        ParseEvent.START: parse_start,
        ParseEvent.METADATA: parse_metadata
    }

    parse(str(game_path), handlers)

    return attributes
