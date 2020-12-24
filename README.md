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

Currently, the package supports organizing the files according to a supplied hierarchy, flattening the files against the supplied root folder, and renaming all the files according to their attributes. Each of these methods takes in an optional `show_progress` boolean parameter which, when true, invokes the presentation of a progress bar indicating the processing of all the game files according to the method.

#### Organize

The `organize` method serves the purpose of moving each game file found (deeply or otherwise) under the root folder to its proper location according to the supplied ordering. If no ordering is given, then treefrog will use the default ordering found in the `treefrog.hierarchy` module. Here is a simple example of calling this method:

```python
from treefrog import Hierarchy, Tree

tree = Tree("slp/", "DTB#566") # Root folder and user's netplay code

ordering = (
    (
        Hierarchy.Member.YEAR,
        Hierarchy.Member.MONTH
    ),
    Hierarchy.Member.OPPONENT_CODE,
    (
        Hierarchy.Member.CHARACTER,
        Hierarchy.Member.OPPONENT_CHARACTER
    ),
    Hierarchy.Member.STAGE,
) # An iterable of the desired levels of the hierarchy

tree.organize(ordering) # Organize the files into subfolders according to the supplied attributes

tree.resolve() # Physically adjust the filesystem to reflect the above change
```

Notice that multiple members may exist on a single level of the hierarchy. The package has some intelligence in place for naming the folders at one of these levels according to the combination of members that are provided. For example, if a level only consists of the `CHARACTER` and `OPPONENT_CHARACTER` members, the folders at that level will be named according to the convention: `CHARACTER vs OPPONENT_CHARACTER`.

Feel free to provide your own logic for formatting the names of the folders at a particular level with a corresponding iterable of functions:

```python
from treefrog import Hierarchy, Tree
from treefrog.format import default_format

tree = Tree("slp/", "DTB#566")

ordering = (
    (
        Hierarchy.Member.YEAR,
        Hierarchy.Member.MONTH
    ),
    Hierarchy.Member.OPPONENT_CODE,
    (
        Hierarchy.Member.CHARACTER,
        Hierarchy.Member.OPPONENT_CHARACTER
    ),
    Hierarchy.Member.STAGE,
)

formatting = (
    lambda year, month: f"{default_format(Hierarchy.Member.MONTH, month)} {year}",
    None,
    lambda *chars: " VS ".join(default_format(Hierarchy.Member.CHARACTER, c) for c in chars),
    None
)

tree.organize(ordering).resolve()
```

If `None` formatting is supplied for a level, then treefrog will resort to the `default_format` function. You can also use this function for a single member as shown in the example at the topmost level.

Further, notice that you can use cascading methods to simplify your programming. Each of the methods `organize`, `flatten`, and `rename` will return a reference to the instance object on which it was called. Something like this: `tree.organize().rename().resolve()` will organize the game files, rename the files, and resolve the physical paths of the files in the order they are called.

#### Flatten

The `flatten` method serves the simple purpose of moving each game file found (deeply or otherwise) under the root folder back to the root folder itself. Here's an example of what calling this method may look like:

```python
from treefrog import Tree

tree = Tree("slp/", "DTB#566")
tree.flatten().resolve()
```

#### Rename

The `rename` method simply renames each game file according to its attributes. Without a rename function supplied, treefrog will use the `default_rename` function found in the `treefrog.format` module. Alternatively, you may provide your own rename function as shown below:

```python
from treefrog import Hierarchy, Tree
from treefrog.format import character_name

def rename(original, members) -> str:
    code = members[Hierarchy.Member.CODE]
    name = members[Hierarchy.Member.NAME]
    character = character_name(members[Hierarchy.Member.CHARACTER])
    opponent_code = members[Hierarchy.Member.OPPONENT_CODE]
    opponent_name = members[Hierarchy.Member.OPPONENT_NAME]
    opponent_character = character_name(members[Hierarchy.Member.OPPONENT_CHARACTER])

    stem = " vs ".join((
        f"[{code}] {name} ({character})",
        f"[{opponent_code}] {opponent_name} ({opponent_character})"
    ))

    return f"{stem}.{original.split('.')[-1]}"

Tree("slp/", "DTB#566").rename().resolve()
```

### Command-Line

This is also command-line program, and can be executed as follows:

```bash
python -m treefrog [-h] -c NETPLAY_CODE [-o | -f] [-r] [-p] ROOT_FOLDER
```

Positional arguments:

```txt
  ROOT_FOLDER           Slippi folder root path
```

Optional arguments:

```txt
  -h, --help            show this help message and exit
  -c NETPLAY_CODE, --netplay-code NETPLAY_CODE
                        Netplay code (e.g. DTB#566)
  -o, --organize        Whether to organize the folder hierarchy
  -f, --flatten         Whether to flatten the folder hierarchy
  -r, --rename          Whether to rename the files according to the game attributes
  -p, --show-progress   Whether to show a progress bar
```

For example, the following command will organize all the game files under the `slp` directory.

```bash
python -m treefrog "slp" -c "DTB#566" -op
```

Feel free to [check out the docs](https://dawsonbooth.com/treefrog/) for more information.

## License

This software is released under the terms of [MIT license](LICENSE).
