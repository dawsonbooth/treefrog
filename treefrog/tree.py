from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import List

from slippi.game import Game
from tqdm import tqdm

from .hierarchy import Hierarchy, game_characteristics
from .parse import Matchup, Month, OpponentNetplayCode, ParseError, Stage, Year
from .rename import create_filename

default_ordering = (
    Year,
    Month,
    OpponentNetplayCode,
    Matchup,
    Stage
)


class Tree:
    root: Path
    sources: List[Path]
    destinations: List[Path]
    netplay_code: str

    def __init__(self, root_folder: str, netplay_code: str):
        self.root = Path(root_folder)
        self.sources = list(self.root.rglob("*.slp"))
        self.destinations = list(p for p in self.sources)
        self.netplay_code = netplay_code

    def organize(
        self,
        ordering: Hierarchy.Ordering = default_ordering,
        show_progress: bool = False
    ) -> Tree:
        destinations = self.destinations
        if show_progress:
            destinations = tqdm(self.destinations, desc="Organize")

        for i, destination in enumerate(destinations):
            self.destinations[i] = self.root
            try:
                game = Game(str(self.sources[i]))

                for parser in ordering:
                    game_attribute = parser(
                        game, netplay_code=self.netplay_code)
                    self.destinations[i] /= str(game_attribute)

                self.destinations[i] /= destination.name

            except ParseError:
                self.destinations[i] /= "Error"
                self.destinations[i] /= destination.name
                continue

        return self

    def flatten(self, show_progress) -> Tree:
        destinations = self.destinations
        if show_progress:
            destinations = tqdm(self.destinations, desc="Flatten")

        for i, destination in enumerate(destinations):
            self.destinations[i] = self.root / destination.name

        return self

    def rename(self, create_filename=create_filename, show_progress=False) -> Tree:
        destinations = self.destinations
        if show_progress:
            destinations = tqdm(self.destinations, desc="Rename")

        for i, destination in enumerate(destinations):
            try:
                characteristics = game_characteristics(
                    str(self.sources[i]), self.netplay_code)
            except ParseError:
                self.destinations[i] = self.root / \
                    "Error" / destination.name
                continue

            self.destinations[i] = destination.parent / \
                create_filename(**characteristics)

        return self

    def resolve(self, show_progress=False) -> Tree:
        destinations = self.destinations
        if show_progress:
            destinations = tqdm(self.destinations, desc="Resolve")

        for i, destination in enumerate(destinations):
            num_duplicates = 0
            new_name = destination.name
            while True:
                renamed = False
                for j, other in enumerate(self.destinations):
                    if new_name == other.name and i != j:
                        num_duplicates += 1
                        renamed = True
                        new_name = f"{destination.stem} ({num_duplicates}){destination.suffix}"

                if not renamed:
                    self.destinations[i] = destination.parent / new_name
                    break

            os.makedirs(destination.parent, exist_ok=True)
            shutil.move(str(self.sources), str(self.destinations[i]))

        for path in self.root.rglob("*"):
            if path.is_dir() and len([f for f in path.rglob("*") if not f.is_dir()]) == 0:
                if path.exists():
                    shutil.rmtree(path)

        return self
