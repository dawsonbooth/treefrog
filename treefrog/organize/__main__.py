import argparse
import sys

from .. import Tree
from ..cli import glob, netplay_code, organize, root_folder, show_progress


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Move your Slippi game files to nested folders according to their features"
    )
    parser.add_argument(*root_folder["name_or_flags"], **root_folder["kwargs"])
    parser.add_argument(*glob["name_or_flags"], **glob["kwargs"])
    parser.add_argument(*netplay_code["name_or_flags"], **netplay_code["kwargs"])
    parser.add_argument(*show_progress["name_or_flags"], **show_progress["kwargs"])

    args = parser.parse_args()

    with Tree(args.root_folder, glob=args.glob, show_progress=args.show_progress) as tree:
        organize(tree, args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
