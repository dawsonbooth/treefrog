
from . import GameFileTree, Hierarchy

if __name__ == "__main__":
    folder_path = "slp"
    netplay_code = "DTB#566"

    tree = GameFileTree(folder_path, netplay_code)

    ordering = (
        Hierarchy.Level.OPPONENT_CODE,
        (
            Hierarchy.Level.CHARACTER,
            Hierarchy.Level.OPPONENT_CHARACTER
        ),
        Hierarchy.Level.STAGE,
    )

    # tree.organize(ordering, show_progress=True)

    tree.flatten(show_progress=True)

    tree.resolve(show_progress=True)
