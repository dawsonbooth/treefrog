from slippi import Game

from .parse import (Character, DateTime, NetplayCode, NetplayName,
                    OpponentCharacter, OpponentNetplayCode,
                    OpponentNetplayName, Stage)

# TODO: Remove reliance on netplay code and use P1/P2 names/codes/characters


def default_filename(source: str, **kwargs) -> str:
    game = Game(source)
    return f"Game_{DateTime(game)}.slp"


def create_filename(source: str, netplay_code: str = None) -> str:
    game = Game(source)

    code = NetplayCode(game, netplay_code=netplay_code)
    name = NetplayName(game, netplay_code=netplay_code)
    character = Character(game, netplay_code=netplay_code)

    opponent_code = OpponentNetplayCode(game, netplay_code=netplay_code)
    opponent_name = OpponentNetplayName(game, netplay_code=netplay_code)
    opponent_character = OpponentCharacter(game, netplay_code=netplay_code)

    timestamp = DateTime(game)
    stage = Stage(game)

    return f"{timestamp} - [{code}] {name} ({character}) vs [{opponent_code}] {opponent_name} ({opponent_character}) - {stage}.slp"
