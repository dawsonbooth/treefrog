from datetime import datetime
from slippi.id import InGameCharacter, Stage


def character_name(character: InGameCharacter) -> str:
    if character == InGameCharacter.DR_MARIO:
        return "Dr. Mario"
    if character == InGameCharacter.GAME_AND_WATCH:
        return "Game & Watch"
    if character in {InGameCharacter.POPO, InGameCharacter.NANA}:
        return "Ice Climbers"
    return character.name.replace("_", " ").title()


def stage_name(stage: Stage) -> str:
    if stage == Stage.FOUNTAIN_OF_DREAMS:
        return "Fountain of Dreams"
    if stage == Stage.YOSHIS_STORY:
        return "Yoshi's Story"
    return stage.name.replace("_", " ").title()


def timestamp(dt: datetime):
    return f"{dt.year}{dt.month:02}{dt.day:02}T{dt.hour:02}{dt.minute:02}{dt.second:02}"
