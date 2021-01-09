from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import List

from slippi.game import Game
from tqdm import tqdm

from .organize import Ordering, build_parent, default_ordering
from .parse import ParseError
from .rename import create_filename


class Tree:
    root: Path
    sources: List[Path]
    destinations: List[Path]

    def __init__(self, root_folder: str):
        self.root = Path(root_folder)
        self.sources = list(self.root.rglob("*.slp"))
        self.destinations = list(p for p in self.sources)

    def organize(
        self,
        ordering: Ordering = default_ordering,
        show_progress: bool = False
    ) -> Tree:
        sources = self.sources
        if show_progress:
            sources = tqdm(sources, desc="Organize")

        for i, source in enumerate(sources):
            try:
                game = Game(str(source))
                rel_path = build_parent(game, ordering) / source.name
            except ParseError:
                rel_path = Path("Error") / source.name

            self.destinations[i] = self.root / rel_path

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
                game = Game(str(self.sources[i]))
                new_name = create_filename(game)
                self.destinations[i] = destination.parent / new_name
            except ParseError:
                self.destinations[i] = self.root / "Error" / destination.name

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
            shutil.move(str(self.sources[i]), str(self.destinations[i]))
            self.sources[i] = self.destinations[i]

        for path in self.root.rglob("*"):
            if path.is_dir() and len([f for f in path.rglob("*") if not f.is_dir()]) == 0:
                if path.exists():
                    shutil.rmtree(path)

        return self
