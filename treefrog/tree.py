from __future__ import annotations

import os
from pathlib import Path
from typing import Callable, Optional, Union

from gibbon import Tree as _Tree
from gibbon.types import T
from slippi.game import Game

from .organize import default_ordering
from .rename import create_filename


class Tree(_Tree):
    def __init__(
        self,
        root_src: Union[str, os.PathLike[str]],
        glob: str = "**/*.slp",
        root_dest: Optional[Union[str, os.PathLike[str]]] = None,
        parse: Optional[Callable[[Path], T]] = Game,
        show_progress: bool = False,
    ) -> None:
        super().__init__(root_src, glob, root_dest, parse, show_progress)

    def organize(self, *ordering) -> Tree:
        if len(ordering) == 0:
            ordering = default_ordering
        return super().organize(*ordering)

    def flatten(self) -> Tree:
        return super().flatten()

    def rename(self, create_filename=create_filename) -> Tree:
        return super().rename(create_filename)
