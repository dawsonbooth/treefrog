import argparse
from pathlib import Path

from . import Hierarchy, Tree

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Organize replay folder')
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
                        help='Whether to rename the files according to the game attributes')

    args = parser.parse_args()

    tree = Tree(args.root_folder, args.netplay_code)

    ordering = (
        Hierarchy.Level.OPPONENT_CODE,
        (
            Hierarchy.Level.CHARACTER,
            Hierarchy.Level.OPPONENT_CHARACTER
        ),
        Hierarchy.Level.STAGE,
    )

    if args.flatten:
        tree.flatten(show_progress=args.show_progress)
    if args.organize:
        tree.organize(ordering, show_progress=args.show_progress)
    if args.rename:
        tree.rename(show_progress=args.show_progress)

    tree.resolve(show_progress=args.show_progress)
