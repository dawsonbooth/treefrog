import calendar
from pathlib import Path
from typing import Any, Dict, Iterable, Union

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


def format_datetime(year: int = None, month: int = None, day: int = None,
                    hour: int = None, minute: int = None, second: int = None):
    date = "-".join(str(d) for d in (month, day, year) if d is not None)
    if year is not None and month is not None:
        date = f"{year} {calendar.month_name[month]}"

    time = "꞉".join(str(t) for t in (hour, minute, second) if t is not None)

    return f"{date} {time}".strip()


def default_format(level: Hierarchy.Level, attributes: Union[Any, Iterable[Any]]) -> str:
    if isinstance(level, Hierarchy.Member):
        member = level
        attribute = attributes

        if member in (Hierarchy.Member.CHARACTER, Hierarchy.Member.OPPONENT_CHARACTER):
            return character_name(attribute)
        elif member == Hierarchy.Member.STAGE:
            return stage_name(attribute)
        elif member == Hierarchy.Member.MONTH:
            return calendar.month_name[attribute]
        return str(attribute)

    elif isinstance(level, Iterable):
        members = sorted(level, key=lambda member: member.value)
        if len(members) == 2:
            if (
                (Hierarchy.Member.NAME in members and Hierarchy.Member.OPPONENT_NAME in members) or
                (Hierarchy.Member.CHARACTER in members and Hierarchy.Member.OPPONENT_CHARACTER) or
                (Hierarchy.Member.CODE in members and Hierarchy.Member.OPPONENT_CODE in members)
            ):
                return f"{default_format(members[0], attributes[0])} vs {default_format(members[1], attributes[1])}"

        if all(
            m in (Hierarchy.Member.YEAR, Hierarchy.Member.MONTH, Hierarchy.Member.DAY,
                  Hierarchy.Member.HOUR, Hierarchy.Member.MINUTE, Hierarchy.Member.SECOND)
            for m in members
        ):
            dt = dict()
            for i, member in enumerate(members):
                attribute = attributes[i]
                if member == Hierarchy.Member.YEAR:
                    dt["year"] = attribute
                elif member == Hierarchy.Member.MONTH:
                    dt["month"] = attribute
                elif member == Hierarchy.Member.DAY:
                    dt["day"] = attribute
                elif member == Hierarchy.Member.HOUR:
                    dt["hour"] = attribute
                elif member == Hierarchy.Member.MINUTE:
                    dt["minute"] = attribute
                elif member == Hierarchy.Member.SECOND:
                    dt["second"] = attribute

            return format_datetime(**dt)

        return " ".join((default_format(members[i], attributes[i]) for i in range(len(members))))


def default_rename(original, members: Dict[Hierarchy.Member, Any]) -> str:
    name, code, character, opponent_name, opponent_code, opponent_character, stage, year, month, day, hour, minute, second = (
        members[k] for k in sorted(members.keys(), key=lambda k: k.value)
    )
    timestamp = f"{year}{month:02}{day:02}T{hour:02}{minute:02}{second:02}"

    players = " vs ".join((
        f"[{code}] {name} ({character_name(character)})",
        f"[{opponent_code}] {opponent_name} ({character_name(opponent_character)})"
    ))

    stem = " - ".join((timestamp, players, stage_name(stage)))

    return stem + Path(original).suffix
