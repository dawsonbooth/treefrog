from pathlib import Path

from .parse.parsers import month, stage, year
from .parse.utils import character_name, most_used_character, opponent, user
from .tree import Tree


def organize(tree: Tree, args):
    if args.netplay_code:
        def opponent_netplay_code(game):
            return opponent(game, args.netplay_code).netplay.code

        def ordered_matchup(game):
            p1 = user(game, args.netplay_code)
            p2 = opponent(game, args.netplay_code)
            return f"{character_name(most_used_character(p1))} vs {character_name(most_used_character(p2))}"

        ordering = (
            year,
            month,
            opponent_netplay_code,
            ordered_matchup,
            stage
        )

        tree.organize(show_progress=args.show_progress, ordering=ordering)
    else:
        tree.organize(show_progress=args.show_progress)


def flatten(tree: Tree, args):
    tree.flatten(show_progress=args.show_progress)


def rename(tree: Tree, args):
    tree.rename(show_progress=args.show_progress)


root_folder = {
    "args": ["root_folder"],
    "kwargs": {
        "type": Path,
        "help": 'Slippi folder root path'
    }
}


netplay_code = {
    "args": ["-c", "--netplay-code"],
    "kwargs": {
        "type": str,
        "help": 'Netplay code (e.g. DTB#566)'
    }
}

show_progress = {
    "args": ["-p", "--show-progress"],
    "kwargs": {
        "action": "store_true",
        "help": 'Whether to show a progress bar'
    }
}