import os
import re
import shutil
from pathlib import Path
from typing import Callable, Iterable, List

from slippi.parse import ParseError
from tqdm import tqdm

from .format import default_format, default_rename
from .hierarchy import Hierarchy, default_ordering, get_attributes


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
        formatting: Iterable[Callable] = None,
        show_progress: bool = False
    ) -> "Tree":
        destinations = self.destinations
        if show_progress:
            destinations = tqdm(self.destinations, desc="Organize")

        for i, destination in enumerate(destinations):
            source = self.sources[i]

            try:
                member_attributes = get_attributes(
                    str(source), self.netplay_code)
            except ParseError:
                self.destinations[i] = self.root / \
                    "Error" / destination.name
                continue

            self.destinations[i] = self.root

            for rank, level in enumerate(ordering):
                if isinstance(level, Hierarchy.Member):
                    attribute = member_attributes[level]

                    if formatting and formatting[rank] is not None:
                        self.destinations[i] /= formatting[rank](attribute)
                    else:
                        self.destinations[i] /= default_format(
                            level, attribute)
                elif isinstance(level, Iterable):
                    attributes = tuple(
                        member_attributes[peer] for peer in level)

                    if formatting and formatting[rank] is not None:
                        self.destinations[i] /= formatting[rank](*attributes)
                    else:
                        self.destinations[i] /= default_format(
                            level, attributes)

            self.destinations[i] /= destination.name

        return self

    def flatten(self, show_progress) -> "Tree":
        destinations = self.destinations
        if show_progress:
            destinations = tqdm(self.destinations, desc="Flatten")

        for i, destination in enumerate(destinations):
            self.destinations[i] = self.root / destination.name

        return self

    def rename(self, rename_func=default_rename, show_progress=False) -> "Tree":
        destinations = self.destinations
        if show_progress:
            destinations = tqdm(self.destinations, desc="Rename")

        for i, destination in enumerate(destinations):
            source = self.sources[i]

            try:
                member_attributes = get_attributes(
                    str(source), self.netplay_code)
            except ParseError:
                self.destinations[i] = self.root / \
                    "Error" / destination.name
                continue

            new_name = rename_func(destination.name, member_attributes)
            new_name = re.sub(r'[\\/:"*?<>|]+', "", new_name)

            self.destinations[i] = destination.parent / new_name

        return self

    def resolve(self, show_progress=False) -> "Tree":
        sources = self.sources
        if show_progress:
            sources = tqdm(self.sources, desc="Resolve")

        for i, source in enumerate(sources):
            destination = self.destinations[i]

            n = 0
            new_name = destination.name
            while True:
                renamed = False
                for j, other in enumerate(self.destinations):
                    if new_name == other.name and i != j:
                        n += 1
                        renamed = True
                        new_name = f"{destination.stem} ({n}){destination.suffix}"

                if not renamed:
                    self.destinations[i] = destination.parent / new_name
                    break

            os.makedirs(destination.parent, exist_ok=True)
            shutil.move(source, self.destinations[i])

        for d in self.root.rglob("*"):
            if d.is_dir() and len([f for f in d.rglob("*") if not f.is_dir()]) == 0:
                if d.exists():
                    shutil.rmtree(d)

        return self
