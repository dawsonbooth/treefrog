

# Example: Plot heat map of neutral wins

from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
import slippi
from slippi.id import Stage
from tqdm import tqdm

# 0. Settings
root_folder = "slp"
netplay_code = "DTB#566"
x, y = list(), list()


# 1. Get games
game_files = [str(p) for p in Path(root_folder).rglob("*.slp")]
games = (slippi.Game(r) for r in game_files)
games = (game for game in games if game.start.stage == Stage.BATTLEFIELD)

for game in tqdm(games):
    # 2. Find ports of players
    port, opponent_port = None, None
    for p, player in enumerate(game.metadata.players):
        if player is not None:
            if player.netplay.code == netplay_code:
                port = p
            else:
                opponent_port = p

    # 3. Get all hits
    opponent_being_hit = False
    for frame in game.frames:
        opponent_frame = frame.ports[opponent_port].leader
        if opponent_being_hit:
            if opponent_frame.post.hit_stun <= 0:
                opponent_being_hit = False
        else:
            if opponent_frame.post.hit_stun > 0:
                opponent_being_hit = True
                pos = frame.ports[port].leader.post.position
                x.append(pos.x)
                y.append(pos.y)


# 4. Plot
sns.set_theme()

sns.scatterplot(x=x, y=y)

plt.show()
