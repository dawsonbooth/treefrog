from typing import Any, Dict

from slippi.id import InGameCharacter, Stage

from .hierarchy import Hierarchy


def character_name(character: InGameCharacter):
    if character == InGameCharacter.DR_MARIO:
        return "Dr. Mario"
    elif character == InGameCharacter.GAME_AND_WATCH:
        return "Game & Watch"
    elif character in {InGameCharacter.POPO, InGameCharacter.NANA}:
        return "Ice Climbers"
    return character.name.replace("_", " ").title()


def stage_name(stage: Stage):
    if stage == Stage.FOUNTAIN_OF_DREAMS:
        return "Fountain of Dreams"
    elif stage == Stage.YOSHIS_STORY:
        return "Yoshi's Story"
    return stage.name.replace("_", " ").title()


def format(*attributes) -> str:
    types = tuple(type(attribute) for attribute in attributes)

    if len(attributes) == 1:
        attribute = attributes[0]

        if isinstance(attribute, InGameCharacter):
            return character_name(attribute)
        elif isinstance(attribute, Stage):
            return stage_name(attribute)
        elif isinstance(attribute, str):
            return attribute

    elif len(attributes) == 2:
        if types.count(InGameCharacter) == 2:
            return f"{character_name(attributes[0])} vs {character_name(attributes[1])}"

    elif len(set(types)) == 1 and types[0] == str:
        return f"{attributes[0]} vs {attributes[1]}"


def rename(name, members: Dict[Hierarchy.Level, Any]):
    return " vs ".join((
        f"[{members[Hierarchy.Level.CODE]}] {members[Hierarchy.Level.NAME]} ({character_name(members[Hierarchy.Level.CHARACTER])})",
        f"[{members[Hierarchy.Level.OPPONENT_CODE]}] {members[Hierarchy.Level.OPPONENT_NAME]} ({character_name(members[Hierarchy.Level.OPPONENT_CHARACTER])})"
    )) + f" - {stage_name(members[Hierarchy.Level.STAGE])}" + f".{name.split('.')[-1]}"
