from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Callable, Dict, List, Tuple, Union

from slippi.game import Game
from tqdm import tqdm

from .organize import Ordering, build_parent, default_ordering
from .parse.utils import games as parse_games
from .rename import create_filename


class Tree:
    root: Path
    glob: str
    show_progress: bool

    sources: Tuple[Path, ...]
    destinations: List[Path]
    operations: Dict[str, Callable[[Path, Game], Path]]
    should_resolve: bool

    def __init__(self, root_folder: Union[str, os.PathLike[str]], glob: str = "**/*.slp", show_progress: bool = False):
        self.root = Path(root_folder)
        self.glob = glob
        self.show_progress = show_progress
        self.reset()

    def reset(self) -> Tree:
        self.sources = tuple(self.root.glob(self.glob))
        self.destinations = list(self.sources)
        self.operations = dict()

        return self

    def organize(self, ordering: Ordering = default_ordering) -> Tree:
        self.operations["organize"] = lambda path, game: self.root / build_parent(game, ordering) / path.name
        self.operations.pop("flatten", None)

        return self

    def flatten(self) -> Tree:
        self.operations["flatten"] = lambda path, _: self.root / path.name
        self.operations.pop("organize", None)

        return self

    def rename(self, create_filename=create_filename) -> Tree:
        self.operations["rename"] = lambda path, game: path.parent / create_filename(game)

        return self

    def resolve(self) -> Tree:
        games = parse_games(self.sources)
        destinations = self.destinations
        if self.show_progress:
            games = tqdm(games, desc="Process games", total=len(self.sources))
            destinations = tqdm(destinations, desc="Move files")

        for i, game in enumerate(games):
            # Perform operations
            try:
                for operation in self.operations.values():
                    self.destinations[i] = operation(self.destinations[i], game)
            except Exception as e:
                self.destinations[i] = self.root / e.__class__.__name__ / self.destinations[i].name

        for i, destination in enumerate(destinations):
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

            # Move file
            os.makedirs(destination.parent, exist_ok=True)
            shutil.move(str(self.sources[i]), str(self.destinations[i]))

        # Remove empty folders
        for path in self.root.rglob("*"):
            if path.is_dir() and len([f for f in path.rglob("*") if not f.is_dir()]) == 0:
                if path.exists():
                    shutil.rmtree(path)

        self.reset()

        return self

    def __enter__(self) -> Tree:
        return self

    def __exit__(self, *args) -> None:
        if None in args:
            self.resolve()
