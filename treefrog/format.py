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


def timestamp(year: int, month: int, day: int, hour: int, minute: int, second: int):
    return f"{year}{month:02}{day:02}T{hour:02}{minute:02}{second:02}"
