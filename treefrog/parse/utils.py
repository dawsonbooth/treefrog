from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Callable, Generator, Optional, Sequence

from slippi import Game
from slippi.id import InGameCharacter, Stage
from slippi.metadata import Metadata
from slippi.parse import ParseError

Parser = Callable[[Game], str]


def _game(path: Path) -> Optional[Game]:
    try:
        return Game(path)
    except ParseError:
        return None


def games(sources: Sequence[Path]) -> Generator[Game, None, None]:
    with ProcessPoolExecutor() as executor:
        for game in executor.map(_game, sources):
            yield game


def ports(game: Game) -> Generator[int, None, None]:
    return (p + 1 for p, player in enumerate(game.metadata.players) if player)


def most_used_character(player: Metadata.Player) -> InGameCharacter:
    return sorted(player.characters.keys(), key=lambda c: player.characters[c])[0]


def players(game: Game) -> Generator[Metadata.Player, None, None]:
    return (game.metadata.players[port - 1] for port in ports(game))


def characters(game: Game) -> Generator[InGameCharacter, None, None]:
    return (most_used_character(player) for player in players(game))


def user(game: Game, netplay_code: str) -> Metadata.Player:
    for player in players(game):
        if player.netplay.code == netplay_code:
            return player


def opponent(game: Game, netplay_code: str) -> Metadata.Player:
    for player in players(game):
        if player.netplay.code != netplay_code:
            return player


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
