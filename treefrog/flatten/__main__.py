import argparse
import sys

from .. import Tree
from ..cli import flatten, root_folder, show_progress


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Rename your Slippi game files according to their features'
    )
    parser.add_argument(*root_folder["args"], **root_folder["kwargs"])
    parser.add_argument(*show_progress["args"], **show_progress["kwargs"])

    args = parser.parse_args()

    tree = Tree(args.root_folder)

    flatten(tree, args)

    tree.resolve(show_progress=args.show_progress)

    return 0


if __name__ == "__main__":
    sys.exit(main())
