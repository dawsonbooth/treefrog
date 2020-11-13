from enum import Enum

from slippi.event import Start
from slippi.metadata import Metadata
from slippi.parse import ParseEvent, parse


class GameAttribute(Enum):
    STAGE = 0
    NAME = 1
    CODE = 2
    CHARACTER = 3
    OPPONENT_NAME = 5
    OPPONENT_CODE = 6
    OPPONENT_CHARACTER = 7


def get_attribute_map(game_path: str, netplay_code: str):
    attributes = {
        GameAttribute.CODE: netplay_code
    }

    def parse_start(start: Start):
        attributes[GameAttribute.STAGE] = start.stage

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
                    attributes[GameAttribute.NAME] = name
                    attributes[GameAttribute.CHARACTER] = character
                else:
                    attributes[GameAttribute.OPPONENT_CODE] = code
                    attributes[GameAttribute.OPPONENT_NAME] = name
                    attributes[GameAttribute.OPPONENT_CHARACTER] = character

    handlers = {
        ParseEvent.START: parse_start,
        ParseEvent.METADATA: parse_metadata
    }

    parse(str(game_path), handlers)

    return attributes
