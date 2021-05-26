from pathlib import Path

from treefrog import Tree
from treefrog.rename import default_filename

root_folder = Path("slp")

original_hierarchy = tuple(root_folder.glob("**/*.slp"))


def restore_hierarchy():
    with Tree(root_folder) as tree:
        tree.flatten().rename(create_filename=default_filename)


def test_flatten():
    with Tree(root_folder) as tree:
        tree.flatten()

    hierarchy = tuple(root_folder.glob("*.slp"))

    assert hierarchy == original_hierarchy

    restore_hierarchy()


def test_rename():
    with Tree(root_folder) as tree:
        tree.rename()

    hierarchy = tuple(root_folder.glob("**/*.slp"))

    assert len(hierarchy) == len(original_hierarchy)
    assert hierarchy != original_hierarchy

    restore_hierarchy()


def test_organize():
    with Tree(root_folder) as tree:
        tree.organize()

    hierarchy = tuple(root_folder.glob("**/*.slp"))

    assert len(hierarchy) == len(original_hierarchy)
    assert hierarchy != original_hierarchy

    restore_hierarchy()
