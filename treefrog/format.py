import calendar
from typing import Optional

from slippi.id import InGameCharacter, Stage

from .hierarchy import Hierarchy


def character_name(character: InGameCharacter) -> str:
    if character == InGameCharacter.DR_MARIO:
        return "Dr. Mario"
    elif character == InGameCharacter.GAME_AND_WATCH:
        return "Game & Watch"
    elif character in {InGameCharacter.POPO, InGameCharacter.NANA}:
        return "Ice Climbers"
    return character.name.replace("_", " ").title()


def stage_name(stage: Stage) -> str:
    if stage == Stage.FOUNTAIN_OF_DREAMS:
        return "Fountain of Dreams"
    elif stage == Stage.YOSHIS_STORY:
        return "Yoshi's Story"
    return stage.name.replace("_", " ").title()


def format_datetime(year: Optional[int] = None, month: Optional[int] = None, day: Optional[int] = None,
                    hour: Optional[int] = None, minute: Optional[int] = None, second: Optional[int] = None):
    date = "-".join(str(d) for d in (month, day, year) if d is not None)
    if year is not None and month is not None:
        date = f"{year} {calendar.month_name[month]}"

    time = "꞉".join(str(t) for t in (hour, minute, second) if t is not None)

    return f"{date} {time}".strip()


def default_format(**kwargs) -> str:
    members, attributes = tuple(kwargs.keys()), tuple(kwargs.values())
    if len(members) == 1:
        member = members[0]
        attribute = attributes[0]

        if member in (Hierarchy.Member.CHARACTER, Hierarchy.Member.OPPONENT_CHARACTER):
            return character_name(attribute)
        elif member == Hierarchy.Member.STAGE:
            return stage_name(attribute)
        elif member == Hierarchy.Member.MONTH:
            return calendar.month_name[attribute]
        return str(attribute)

    if len(members) == 2 and set(members) in (
        {Hierarchy.Member.NAME, Hierarchy.Member.OPPONENT_NAME},
        {Hierarchy.Member.CHARACTER, Hierarchy.Member.OPPONENT_CHARACTER},
        {Hierarchy.Member.CODE, Hierarchy.Member.OPPONENT_CODE}
    ):
        return " vs ".join((default_format(**{member: attribute}) for member, attribute in kwargs.items()))

    if all(m in {
        Hierarchy.Member.YEAR, Hierarchy.Member.MONTH, Hierarchy.Member.DAY,
        Hierarchy.Member.HOUR, Hierarchy.Member.MINUTE, Hierarchy.Member.SECOND
    } for m in members):
        return format_datetime(**kwargs)

    return " ".join((default_format(**{member: attribute}) for member, attribute in kwargs.items()))


def default_rename(
    name: str, code: str, character: InGameCharacter,
    opponent_name: str, opponent_code: str, opponent_character: InGameCharacter,
    stage: Stage, year: int, month: int, day: int, hour: int, minute: int, second: int
) -> str:
    timestamp = f"{year}{month:02}{day:02}T{hour:02}{minute:02}{second:02}"

    players = " vs ".join((
        f"[{code}] {name} ({character_name(character)})",
        f"[{opponent_code}] {opponent_name} ({character_name(opponent_character)})"
    ))

    return " - ".join((timestamp, players, stage_name(stage))) + ".slp"
