import argparse
import sys

from .. import Tree
from ..cli import default_rename, glob, rename, root_folder, show_progress


def main() -> int:
    parser = argparse.ArgumentParser(description="Flatten your Slippi game files to a shared parent folder")
    parser.add_argument(*root_folder["name_or_flags"], **root_folder["kwargs"])
    parser.add_argument(*glob["name_or_flags"], **glob["kwargs"])
    parser.add_argument(*show_progress["name_or_flags"], **show_progress["kwargs"])
    parser.add_argument(*default_rename["name_or_flags"], **default_rename["kwargs"])

    args = parser.parse_args()

    with Tree(args.root_folder, glob=args.glob, show_progress=args.show_progress) as tree:
        rename(tree, args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
