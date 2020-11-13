import shutil
import os
from enum import Enum
from pathlib import Path
from typing import Iterable, List, Tuple
from slippi.event import Start
from slippi.metadata import Metadata
from slippi.parse import parse, ParseEvent
from tqdm import tqdm


class ReplayAttribute(Enum):
    STAGE = 0
    NAME = 1
    CODE = 2
    CHARACTER = 3
    OPPONENT_NAME = 5
    OPPONENT_CODE = 6
    OPPONENT_CHARACTER = 7


default_precedence = (
    ReplayAttribute.OPPONENT_CODE,
    (
        ReplayAttribute.CHARACTER,
        ReplayAttribute.OPPONENT_CHARACTER
    ),
    ReplayAttribute.STAGE
)


def get_attributes(replay_path: str, netplay_code: str):
    attributes = {
        ReplayAttribute.CODE: netplay_code
    }

    def parse_start(start: Start):
        attributes[ReplayAttribute.STAGE] = start.stage.name

    def parse_metadata(metadata: Metadata):
        for player in metadata.players:
            if player is not None:
                if player.netplay.code == netplay_code:
                    attributes[ReplayAttribute.NAME] = player.netplay.name
                    attributes[ReplayAttribute.CHARACTER] = sorted(
                        player.characters.keys(),
                        key=lambda c: player.characters[c]
                    )[0].name  # TODO: Prettify string
                else:
                    attributes[ReplayAttribute.OPPONENT_CODE] = player.netplay.code
                    attributes[ReplayAttribute.OPPONENT_NAME] = player.netplay.name
                    attributes[ReplayAttribute.OPPONENT_CHARACTER] = sorted(
                        player.characters.keys(),
                        key=lambda c: player.characters[c]
                    )[0].name  # TODO: Prettify string

    handlers = {
        ParseEvent.START: parse_start,
        ParseEvent.METADATA: parse_metadata
    }

    parse(str(replay_path), handlers)

    return attributes


class ReplayFileTree:
    root: Path
    sources: List[Path]
    destinations: List[Path]
    netplay_code: str

    def __init__(self, replay_folder: str, netplay_code: str):
        self.root = Path(replay_folder)
        self.sources = list(self.root.rglob("*.slp"))
        self.destinations = list(p for p in self.sources)

        self.netplay_code = netplay_code

    def organize(self, precedence=default_precedence):
        for i, source in enumerate(tqdm(self.sources)):  # TODO: Remove progress
            attributes = get_attributes(source, self.netplay_code)

            self.destinations[i] = self.root

            for a_type in precedence:
                if isinstance(a_type, ReplayAttribute):
                    self.destinations[i] /= attributes[a_type]
                elif isinstance(a_type, Iterable):
                    # TODO: Format string based on attributes
                    self.destinations[i] /= " vs ".join(
                        attributes[a_type] for a_type in a_type
                    )

            self.destinations[i] /= source.parts[-1]

    def flatten(self):
        for i, source in enumerate(self.sources):
            self.destinations[i] = self.root / source.parts[-1]

    def resolve(self):
        for i, source in enumerate(self.sources):
            destination = self.destinations[i]
            os.makedirs(destination.parent, exist_ok=True)
            shutil.move(source, destination)

        for f in self.root.rglob("*"):
            if f.is_dir() and len(list(f.rglob("*.slp"))) == 0:
                shutil.rmtree(f)
