from enum import Enum
from typing import Any, Dict, Iterable, Sequence

from slippi.event import Start
from slippi.metadata import Metadata
from slippi.parse import ParseEvent, parse


class Hierarchy():
    class Member(str, Enum):
        NAME = "name"
        CODE = "code"
        CHARACTER = "character"
        OPPONENT_NAME = "opponent_name"
        OPPONENT_CODE = "opponent_code"
        OPPONENT_CHARACTER = "opponent_character"
        STAGE = "stage"
        YEAR = "year"
        MONTH = "month"
        DAY = "day"
        HOUR = "hour"
        MINUTE = "minute"
        SECOND = "second"

    Level = Iterable[Member]
    Ordering = Sequence[Level]


def get_attributes(game_path: str, netplay_code: str) -> Dict[Hierarchy.Member, Any]:
    game_attributes: Dict[Hierarchy.Member, Any] = {
        Hierarchy.Member.CODE: netplay_code
    }

    def parse_start(start: Start):
        game_attributes[Hierarchy.Member.STAGE] = start.stage

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
                    game_attributes[Hierarchy.Member.NAME] = name
                    game_attributes[Hierarchy.Member.CHARACTER] = character
                else:
                    game_attributes[Hierarchy.Member.OPPONENT_CODE] = code
                    game_attributes[Hierarchy.Member.OPPONENT_NAME] = name
                    game_attributes[Hierarchy.Member.OPPONENT_CHARACTER] = character
        game_attributes[Hierarchy.Member.YEAR] = metadata.date.year
        game_attributes[Hierarchy.Member.MONTH] = metadata.date.month
        game_attributes[Hierarchy.Member.DAY] = metadata.date.day
        game_attributes[Hierarchy.Member.HOUR] = metadata.date.hour
        game_attributes[Hierarchy.Member.MINUTE] = metadata.date.minute
        game_attributes[Hierarchy.Member.SECOND] = metadata.date.second

    handlers = {
        ParseEvent.START: parse_start,
        ParseEvent.METADATA: parse_metadata
    }

    parse(game_path, handlers)

    return game_attributes


default_ordering: Hierarchy.Ordering = (
    {
        Hierarchy.Member.YEAR,
        Hierarchy.Member.MONTH
    },
    {
        Hierarchy.Member.OPPONENT_CODE
    },
    {
        Hierarchy.Member.CHARACTER,
        Hierarchy.Member.OPPONENT_CHARACTER
    },
    {
        Hierarchy.Member.STAGE
    },
)
