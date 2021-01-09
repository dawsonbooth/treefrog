import argparse
import sys
from pathlib import Path

from . import Tree
from .parse.parsers import matchup, month, stage, year
from .parse.utils import opponent


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Organize the Slippi game files in your filesystem according to their attributes'
    )
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('root_folder', type=Path,
                        help='Slippi folder root path')
    parser.add_argument('-c', '--netplay-code', type=str, required=True,
                        help='Netplay code (e.g. DTB#566)')
    group.add_argument('-o', '--organize', action='store_true',
                       help='Whether to organize the folder hierarchy')
    group.add_argument('-f', '--flatten', action='store_true',
                       help='Whether to flatten the folder hierarchy')
    parser.add_argument('-r', '--rename', action='store_true',
                        help='Whether to rename the files according to the game attributes')
    parser.add_argument('-p', '--show-progress', action='store_true',
                        help='Whether to show a progress bar')

    args = parser.parse_args()

    tree = Tree(args.root_folder)

    if args.flatten:
        tree.flatten(show_progress=args.show_progress)
    if args.organize:
        def opponent_netplay_code(game):
            return opponent(game, args.netplay_code).netplay.code

        ordering = (  # TODO: Use this only if *optional* netplay code is provided, otherwise default
            year,
            month,
            opponent_netplay_code,
            matchup,
            stage
        )

        tree.organize(show_progress=args.show_progress, ordering=ordering)
    if args.rename:
        tree.rename(show_progress=args.show_progress)

    tree.resolve(show_progress=args.show_progress)

    return 0


if __name__ == "__main__":
    sys.exit(main())
