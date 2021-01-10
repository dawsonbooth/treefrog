from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import List, Tuple

from slippi.game import Game
from tqdm import tqdm

from .organize import Ordering, build_parent, default_ordering
from .rename import create_filename


class Tree:
    root: Path
    sources: Tuple[Path]
    destinations: List[Path]

    def __init__(self, root_folder: str | os.PathLike[str]):
        self.root = Path(root_folder)
        self.sources = tuple(self.root.rglob("*.slp"))
        self.destinations = list(self.sources)

    def organize(self, ordering: Ordering = default_ordering) -> Tree:
        for i, destination in enumerate(self.destinations):
            game = Game(self.sources[i])
            parent = build_parent(game, ordering)
            self.destinations[i] = self.root / parent / destination.name

        return self

    def flatten(self) -> Tree:
        for i, destination in enumerate(self.destinations):
            self.destinations[i] = self.root / destination.name

        return self

    def rename(self, create_filename=create_filename) -> Tree:
        for i, destination in enumerate(self.destinations):
            game = Game(self.sources[i])
            self.destinations[i] = destination.parent / create_filename(game)

        return self

    def resolve(self, show_progress=False) -> Tree:
        destinations = self.destinations
        if show_progress:
            destinations = tqdm(self.destinations, desc="Resolve")

        for i, destination in enumerate(destinations):
            # Perform operations
            # TODO

            # Rename if duplicate
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

            # Move
            os.makedirs(destination.parent, exist_ok=True)
            shutil.move(str(self.sources[i]), str(self.destinations[i]))

        self.sources = tuple(self.destinations)

        for path in self.root.rglob("*"):
            if path.is_dir() and len([f for f in path.rglob("*") if not f.is_dir()]) == 0:
                if path.exists():
                    shutil.rmtree(path)

        return self
