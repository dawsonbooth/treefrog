from pathlib import Path
from treefrog.rename import default_filename
from treefrog import Tree


root_folder = Path("slp")

original_hierarchy = tuple(root_folder.rglob("*.slp"))


def restore_tree(tree: Tree):
    tree.flatten().rename(create_filename=default_filename).resolve()


def test_flatten():
    tree = Tree(root_folder)
    tree.flatten().resolve()
    hierarchy = tuple(root_folder.rglob("*.slp"))

    assert len(hierarchy) == len(original_hierarchy)
    assert hierarchy != original_hierarchy

    restore_tree(tree)


def test_rename():
    tree = Tree(root_folder)
    tree.rename().resolve()
    hierarchy = tuple(root_folder.rglob("*.slp"))

    assert len(hierarchy) == len(original_hierarchy)
    assert hierarchy != original_hierarchy

    restore_tree(tree)


def test_organize():
    tree = Tree(root_folder)
    tree.organize().resolve()
    hierarchy = tuple(root_folder.rglob("*.slp"))

    assert len(hierarchy) == len(original_hierarchy)
    assert hierarchy != original_hierarchy

    restore_tree(tree)
