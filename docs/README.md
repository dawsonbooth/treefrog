# `treefrog`

[![](https://img.shields.io/pypi/v/treefrog.svg?style=flat)](https://pypi.org/pypi/treefrog/)
[![](https://img.shields.io/pypi/dw/treefrog.svg?style=flat)](https://pypi.org/pypi/treefrog/)
[![](https://img.shields.io/pypi/pyversions/treefrog.svg?style=flat)](https://pypi.org/pypi/treefrog/)
[![](https://img.shields.io/pypi/format/treefrog.svg?style=flat)](https://pypi.org/pypi/treefrog/)
[![](https://img.shields.io/pypi/l/treefrog.svg?style=flat)](https://github.com/dawsonbooth/treefrog/blob/master/LICENSE)

## Description

Organize the Slippi game files in your filesystem according to their attributes.

## Installation

With [Python](https://www.python.org/downloads/) installed, simply run the following command to add the package to your project.

```bash
pip install treefrog
```

## Usage

### Module

Currently, the package supports organizing the files according to a supplied ordering of parsers, flattening the files against the supplied root folder, and renaming all the files according to their attributes. These may be accomplished programmatically with the use of the `Tree` class or through the command-line interface.

#### Organize

The `organize` method serves the purpose of moving each game file found (deeply or otherwise) under the root folder to its proper location according to the supplied ordering of parsers. If no ordering is given, then treefrog will use its default. Here is a simple example of calling this method:

```python
from treefrog import Tree
from treefrog.parse.parsers import year, month, matchup, stage

ordering = (
    year,
    month,
    matchup,
    stage
) # An iterable of the desired levels of the hierarchy

with Tree("slp/", show_progress=True) as tree:
    tree.organize(ordering) # Organize the files into subfolders according to the supplied attributes
```

Feel free to provide your own logic for formatting the names of the folders at a particular level with a corresponding iterable of functions:

```python
from treefrog import Tree
from treefrog.parse.parsers import year, month, stage
from treefrog.parse.utils import character_name, most_used_character, opponent, user

def ordered_matchup(game):
    p1 = user(game, "DTB#566")
    p2 = opponent(game, "DTB#566")
    return f"{character_name(most_used_character(p1))} vs {character_name(most_used_character(p2))}"

ordering = (
    year,
    month,
    lambda game: opponent(game, "DTB#566").netplay.code,
    ordered_matchup,
    stage
)

with Tree("slp/", show_progress=True) as tree:
    tree.organize(ordering)
```

Any custom parser you provide will need to be a `Callable` that takes in a `Game` instance and returns a `str`.

Further, you can use cascading methods to simplify your programming. Each of the methods `organize`, `flatten`, and `rename` will return a reference to the instance object on which it was called. Something like this: `tree.organize().rename()` will both organize and rename the game files.

#### Flatten

The `flatten` method serves the simple purpose of moving each game file found (deeply or otherwise) under the root folder back to the root folder itself. Here's an example of what calling this method may look like:

```python
from treefrog import Tree

tree = Tree("slp/")
tree.flatten().resolve()
```

Note that you do not have to use `Tree` with a context manager. If you do not use the `with` keyword as in the first couple of examples, you will need to end your operations with a call to the `resolve` method in order to see the changes reflected in your filesystem.

#### Rename

The `rename` method simply renames each game file according to its attributes. Without a rename function supplied, treefrog will use the `default_filename` function found in the `treefrog.rename` module. Alternatively, you may provide your own rename function as shown below:

```python
from treefrog import Tree
from treefrog.parse.parsers import stage, timestamp
from treefrog.parse.utils import character_name, characters

def create_filename(game: Game):
    p1, p2 = tuple(characters(game))
    return f"{timestamp(game)} - {character_name(p1)} vs {character_name(p2)} - {stage(game)}.slp"

with Tree("slp/") as tree:
    tree.rename(create_filename=create_filename)
```

### Command-Line

This is also command-line program, and can be executed as follows:

```txt
python -m treefrog [-h] [-c NETPLAY_CODE] [-p] [-d] [-o | -f] [-r] root_folder
```

Positional arguments:

```txt
  root_folder           Slippi folder root path
```

Optional arguments:

```txt
  -h, --help            show this help message and exit
  -c NETPLAY_CODE, --netplay-code NETPLAY_CODE
                        Netplay code (e.g. DTB#566)
  -p, --show-progress   Whether to show a progress bar
  -d, --default-rename  Whether to restore the filenames to their defaults
  -o, --organize        Whether to organize the folder hierarchy
  -f, --flatten         Whether to flatten your Slippi game files to a shared parent folder
  -r, --rename          Whether to rename the files according to their features
```

For example, the following command will organize all the game files under the `slp` directory with a progress bar.

```bash
python -m treefrog "slp" -c "DTB#566" -op
```

Feel free to [check out the docs](https://dawsonbooth.com/treefrog/) for more information.

## License

This software is released under the terms of [MIT license](LICENSE).
