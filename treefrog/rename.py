from slippi.id import InGameCharacter, Stage

from .format import character_name, stage_name, timestamp


def default_filename(
    year: int, month: int, day: int, hour: int, minute: int, second: int, **kwargs
) -> str:
    return f"Game_{timestamp(year, month, day, hour, minute, second)}.slp"


def create_filename(
    name: str, code: str, character: InGameCharacter,
    opponent_name: str, opponent_code: str, opponent_character: InGameCharacter,
    stage: Stage, year: int, month: int, day: int, hour: int, minute: int, second: int
) -> str:
    players = " vs ".join((
        f"[{code}] {name} ({character_name(character)})",
        f"[{opponent_code}] {opponent_name} ({character_name(opponent_character)})"
    ))

    return " - ".join((timestamp(year, month, day, hour, minute, second), players, stage_name(stage))) + ".slp"
