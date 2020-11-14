import os
import re
import shutil
from pathlib import Path
from typing import Callable, Iterable, List

from slippi.parse import ParseError
from tqdm import tqdm

from .format import format as default_format
from .format import rename as default_rename
from .hierarchy import Hierarchy, default_ordering, get_members


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
        format: Iterable[Callable] = None,
        show_progress: bool = False
    ):
        destinations = self.destinations
        if show_progress:
            destinations = tqdm(self.destinations, desc="Organize")

        for i, destination in enumerate(destinations):
            source = self.sources[i]

            try:
                members = get_members(source, self.netplay_code)
            except ParseError:
                self.destinations[i] = self.root / \
                    "Error" / destination.name
                continue

            self.destinations[i] = self.root

            for rank, level in enumerate(ordering):
                if isinstance(level, Hierarchy.Level):
                    attribute = members[level]

                    if format and format[rank]:
                        self.destinations[i] /= format[rank](attribute)
                    else:
                        self.destinations[i] /= default_format(attribute)
                elif isinstance(level, Iterable) and not isinstance(level, str):
                    peers = level
                    attributes = ((members[peer] for peer in peers))

                    if format and format[rank]:
                        self.destinations[i] /= format[rank](*attributes)
                    else:
                        self.destinations[i] /= default_format(*attributes)

            self.destinations[i] /= destination.name

    def flatten(self, show_progress):
        destinations = self.destinations
        if show_progress:
            destinations = tqdm(self.destinations, desc="Flatten")

        for i, destination in enumerate(destinations):
            self.destinations[i] = self.root / destination.name

    def rename(self, rename_func=default_rename, show_progress=False):
        destinations = self.destinations
        if show_progress:
            destinations = tqdm(self.destinations, desc="Rename")

        for i, destination in enumerate(destinations):
            source = self.sources[i]

            try:
                members = get_members(source, self.netplay_code)
            except ParseError:
                self.destinations[i] = self.root / \
                    "Error" / destination.name
                continue

            new_name = rename_func(destination.name, members)
            new_name = re.sub(r'[\\/:"*?<>|]+', "", new_name)

            self.destinations[i] = destination.parent / new_name

    def resolve(self, show_progress=False):
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

        for f in self.root.rglob("*"):
            if f.is_dir() and len(tuple(f.rglob("*.slp"))) == 0:
                shutil.rmtree(f)
