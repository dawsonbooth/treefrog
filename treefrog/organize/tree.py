import os
import shutil
from pathlib import Path
from typing import Callable, Iterable, List, Union

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
        rename: Union[Callable, bool] = None,
        show_progress: bool = False
    ):
        sources = self.sources
        if show_progress:
            sources = tqdm(self.sources)

        for i, source in enumerate(sources):
            members = get_members(source, self.netplay_code)

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

            if rename is not None:
                if isinstance(rename, Callable):
                    self.destinations[i] /= rename(source.name, members)
                elif isinstance(rename, bool) and rename:
                    self.destinations[i] /= default_rename(
                        source.name, members
                    )
            else:
                self.destinations[i] /= source.name

    def flatten(self, show_progress):
        sources = self.sources
        if show_progress:
            sources = tqdm(self.sources)

        for i, source in enumerate(sources):
            self.destinations[i] = self.root / source.name

    def resolve(self, show_progress=False):
        sources = self.sources
        if show_progress:
            sources = tqdm(self.sources)

        for i, source in enumerate(sources):
            destination = self.destinations[i]
            os.makedirs(destination.parent, exist_ok=True)
            shutil.move(source, destination)

        for f in self.root.rglob("*"):
            if f.is_dir() and len(tuple(f.rglob("*.slp"))) == 0:
                shutil.rmtree(f)