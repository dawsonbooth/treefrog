from pathlib import Path
from treefrog.rename import default_filename
from treefrog import Tree


root_folder = Path("slp")


def restore_tree(tree: Tree):
    tree.flatten().rename(create_filename=default_filename).resolve()


def test_flatten():
    tree = Tree(root_folder)
    tree.flatten().resolve()

    assert len(list(root_folder.glob("*.slp"))) == 36

    restore_tree(tree)


def test_rename():
    tree = Tree(root_folder)
    tree.rename().resolve()

    assert len(list(root_folder.glob("*.slp"))) == 36

    restore_tree(tree)


def test_organize():
    tree = Tree(root_folder)
    tree.organize().resolve()

    assert len(list(root_folder.rglob("*.slp"))) == 36

    restore_tree(tree)
