import argparse
import sys

from .. import Tree
from ..cli import flatten, glob, root_folder, show_progress


def main() -> int:
    parser = argparse.ArgumentParser(description="Rename your Slippi game files according to their features")
    parser.add_argument(*root_folder["name_or_flags"], **root_folder["kwargs"])
    parser.add_argument(*glob["name_or_flags"], **glob["kwargs"])
    parser.add_argument(*show_progress["name_or_flags"], **show_progress["kwargs"])

    args = parser.parse_args()

    with Tree(args.root_folder, glob=args.glob, show_progress=args.show_progress) as tree:
        flatten(tree, args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
