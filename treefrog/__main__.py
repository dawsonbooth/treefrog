import argparse
import sys

from . import Tree
from .cli import default_rename, flatten, netplay_code, organize, rename, root_folder, show_progress


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Organize the Slippi game files in your filesystem according to their attributes"
    )
    group = parser.add_mutually_exclusive_group()
    parser.add_argument(*root_folder["args"], **root_folder["kwargs"])
    parser.add_argument(*netplay_code["args"], **netplay_code["kwargs"])
    parser.add_argument(*show_progress["args"], **show_progress["kwargs"])
    parser.add_argument(*default_rename["args"], **default_rename["kwargs"])
    group.add_argument("-o", "--organize", action="store_true", help="Whether to organize the folder hierarchy")
    group.add_argument(
        "-f",
        "--flatten",
        action="store_true",
        help="Whether to flatten your Slippi game files to a shared parent folder",
    )
    parser.add_argument(
        "-r", "--rename", action="store_true", help="Whether to rename the files according to their features"
    )

    args = parser.parse_args()

    with Tree(args.root_folder, show_progress=args.show_progress) as tree:
        if args.flatten:
            flatten(tree, args)
        if args.organize:
            organize(tree, args)
        if args.rename:
            rename(tree, args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
