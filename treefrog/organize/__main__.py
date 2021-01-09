import argparse
import sys

from .. import Tree
from ..cli import netplay_code, organize, root_folder, show_progress


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Move your Slippi game files to nested folders according to their features'
    )
    parser.add_argument(*root_folder["args"], **root_folder["kwargs"])
    parser.add_argument(*netplay_code["args"], **netplay_code["kwargs"])
    parser.add_argument(*show_progress["args"], **show_progress["kwargs"])

    args = parser.parse_args()

    tree = Tree(args.root_folder)

    organize(tree, args)

    tree.resolve(show_progress=args.show_progress)

    return 0


if __name__ == "__main__":
    sys.exit(main())
