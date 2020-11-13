
from . import ReplayFileTree

if __name__ == "__main__":
    folder_path = "slp"
    netplay_code = "DTB#566"

    tree = ReplayFileTree(folder_path, netplay_code)

    tree.flatten()

    tree.resolve()
