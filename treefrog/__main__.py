from slippi.id import InGameCharacter
from slippi.parse import ParseEvent

from . import games, select

# TODO: Ideal kind of query -- make this bad boy work fast
select(game.metadata for game in games("slp") if game.metadata.players[0].characters[0] == InGameCharacter.FALCO)
