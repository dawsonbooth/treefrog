import os
import shutil
from pathlib import Path
from typing import Iterable, List

from tqdm import tqdm

from .attribute import GameAttribute, get_attribute_map
from .format import format as default_format

default_hierarchy = (
    GameAttribute.OPPONENT_CODE,
    (
        GameAttribute.CHARACTER,
        GameAttribute.OPPONENT_CHARACTER
    ),
    GameAttribute.STAGE
)


class GameFileTree:
    root: Path
    sources: List[Path]
    destinations: List[Path]
    netplay_code: str

    def __init__(self, root_folder: str, netplay_code: str):
        self.root = Path(root_folder)
        self.sources = list(self.root.rglob("*.slp"))
        self.destinations = list(p for p in self.sources)
        self.netplay_code = netplay_code

    def organize(self, hierarchy=default_hierarchy, format=None, show_progress=False):
        sources = self.sources
        if show_progress:
            sources = tqdm(self.sources)

        for i, source in enumerate(sources):
            attribute_map = get_attribute_map(source, self.netplay_code)

            self.destinations[i] = self.root

            for j, level in enumerate(hierarchy):
                attributes = None
                if isinstance(level, GameAttribute):
                    attributes = (attribute_map[level],)
                elif isinstance(level, Iterable) and not isinstance(level, str):
                    attributes = ((attribute_map[a_type] for a_type in level))

                folder_name = ""
                if format and format[j]:
                    folder_name = format[j](*attributes)
                else:
                    folder_name = default_format(*attributes)

                self.destinations[i] /= folder_name

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
            if f.is_dir() and len(list(f.rglob("*.slp"))) == 0:
                shutil.rmtree(f)
