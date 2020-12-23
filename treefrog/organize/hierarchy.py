from enum import Enum, auto
from typing import Any, Dict, Iterable, Union

from slippi.event import Start
from slippi.metadata import Metadata
from slippi.parse import ParseEvent, parse


class Hierarchy():
    class Member(Enum):
        NAME = auto()
        CODE = auto()
        CHARACTER = auto()
        OPPONENT_NAME = auto()
        OPPONENT_CODE = auto()
        OPPONENT_CHARACTER = auto()
        STAGE = auto()
        YEAR = auto()
        MONTH = auto()
        DAY = auto()
        HOUR = auto()
        MINUTE = auto()
        SECOND = auto()

    Level = Union[Member, Iterable[Member]]
    Ordering = Iterable[Level]


def get_attributes(game_path: str, netplay_code: str) -> Dict[Hierarchy.Member, Any]:
    members: Dict[Hierarchy.Member, Any] = {
        Hierarchy.Member.CODE: netplay_code
    }

    def parse_start(start: Start):
        members[Hierarchy.Member.STAGE] = start.stage

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
                    members[Hierarchy.Member.NAME] = name
                    members[Hierarchy.Member.CHARACTER] = character
                else:
                    members[Hierarchy.Member.OPPONENT_CODE] = code
                    members[Hierarchy.Member.OPPONENT_NAME] = name
                    members[Hierarchy.Member.OPPONENT_CHARACTER] = character
        members[Hierarchy.Member.YEAR] = metadata.date.year
        members[Hierarchy.Member.MONTH] = metadata.date.month
        members[Hierarchy.Member.DAY] = metadata.date.day
        members[Hierarchy.Member.HOUR] = metadata.date.hour
        members[Hierarchy.Member.MINUTE] = metadata.date.minute
        members[Hierarchy.Member.SECOND] = metadata.date.second

    handlers = {
        ParseEvent.START: parse_start,
        ParseEvent.METADATA: parse_metadata
    }

    parse(game_path, handlers)

    return members


default_ordering = (
    (
        Hierarchy.Member.YEAR,
        Hierarchy.Member.MONTH
    ),
    Hierarchy.Member.OPPONENT_CODE,
    (
        Hierarchy.Member.CHARACTER,
        Hierarchy.Member.OPPONENT_CHARACTER
    ),
    Hierarchy.Member.STAGE,
)
