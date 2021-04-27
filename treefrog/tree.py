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


def safe_move(source: Path, destination: Path) -> None:
    if source == destination:
        return

    if not destination.parent.exists():
        os.makedirs(destination.parent)
        shutil.move(str(source), str(destination))
        return

    if not destination.exists():
        shutil.move(str(source), str(destination))
        return

    stem, suffix = destination.stem, destination.suffix
    destination = destination.parent / f"{stem} (1){suffix}"

    i = 1
    while destination.exists():
        destination = destination.parent / f"{stem} ({i}){suffix}"
        i += 1

    shutil.move(str(source), str(destination))


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
        # Perform operations
        games = parse_games(self.sources)
        if self.show_progress:
            games = tqdm(games, desc="Process games", total=len(self.sources))

        for i, game in enumerate(games):
            try:
                for operation in self.operations.values():
                    self.destinations[i] = operation(self.destinations[i], game)
            except Exception as e:
                self.destinations[i] = self.root / e.__class__.__name__ / self.destinations[i].name

        # Move files
        paths = zip(self.sources, self.destinations)
        if self.show_progress:
            paths = tqdm(paths, desc="Move files", total=len(self.sources))

        for source, destination in paths:
            safe_move(source, destination)

        # Remove empty source folders
        processed_folders = set()
        for source in tqdm(self.sources):
            parents = list(source.parents)
            for parent in parents[parents.index(self.root) :]:
                if parent not in processed_folders and len([f for f in parent.rglob("*") if not f.is_dir()]) == 0:
                    shutil.rmtree(parent)
                processed_folders.add(parent)

        self.reset()

        return self

    def __enter__(self) -> Tree:
        return self

    def __exit__(self, *args) -> None:
        if None in args:
            self.resolve()
