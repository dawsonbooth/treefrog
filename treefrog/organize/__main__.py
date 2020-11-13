
from . import GameFileTree, GameAttribute

if __name__ == "__main__":
    folder_path = "slp"
    netplay_code = "DTB#566"

    tree = GameFileTree(folder_path, netplay_code)

    hierarchy = (
        GameAttribute.STAGE,
        (
            GameAttribute.CHARACTER,
            GameAttribute.OPPONENT_CHARACTER
        ),
        GameAttribute.OPPONENT_CODE
    )

    # tree.organize(hierarchy, show_progress=True)

    tree.flatten(show_progress=True)

    tree.resolve(show_progress=True)
