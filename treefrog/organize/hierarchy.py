from enum import Enum, auto
from typing import Any, Dict, Iterable, Union

from slippi.event import Start
from slippi.metadata import Metadata
from slippi.parse import ParseEvent, parse


class Hierarchy():
    class Level(Enum):
        STAGE = auto()
        NAME = auto()
        CODE = auto()
        CHARACTER = auto()
        OPPONENT_NAME = auto()
        OPPONENT_CODE = auto()
        OPPONENT_CHARACTER = auto()

    Ordering = Iterable[Union[Level, Iterable[Level]]]


def get_members(game_path: str, netplay_code: str) -> Dict[Hierarchy.Level, Any]:
    members: Dict[Hierarchy.Level, Any] = {
        Hierarchy.Level.CODE: netplay_code
    }

    def parse_start(start: Start):
        members[Hierarchy.Level.STAGE] = start.stage

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
                    members[Hierarchy.Level.NAME] = name
                    members[Hierarchy.Level.CHARACTER] = character
                else:
                    members[Hierarchy.Level.OPPONENT_CODE] = code
                    members[Hierarchy.Level.OPPONENT_NAME] = name
                    members[Hierarchy.Level.OPPONENT_CHARACTER] = character

    handlers = {
        ParseEvent.START: parse_start,
        ParseEvent.METADATA: parse_metadata
    }

    parse(str(game_path), handlers)

    return members


default_ordering: Hierarchy.Ordering = (
    Hierarchy.Level.OPPONENT_CODE,
    (
        Hierarchy.Level.CHARACTER,
        Hierarchy.Level.OPPONENT_CHARACTER
    ),
    Hierarchy.Level.STAGE
)
