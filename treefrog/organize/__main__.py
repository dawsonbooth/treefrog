from . import Hierarchy, Tree

if __name__ == "__main__":
    root_folder = "slp"
    netplay_code = "DTB#566"

    tree = Tree(root_folder, netplay_code)

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
