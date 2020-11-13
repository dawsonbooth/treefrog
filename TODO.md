# TODO

## Use Cases

### Search

Query a game for a specific event.

#### Applications

- Find all hits
  - Find all neutral wins/losses
  - Find all punish continuations
  - Find all punish reversals
- Find all guaranteed KOs and missed opportunity
- Find best mixups
- Find recommended strategies
  - What should I do at high percent vs fox on battlefield?
    - Positions and options
    - Go under side platform and mixup dash dance, forward air, and downtilt

#### Example Code

```python
select(GameEvent.HIT, game, limit=3)
```

### Plot

#### Parameters

- Stage (background image)
- Show blast zones (boolean)

#### Applications

- Heat map
  - Neutral exchanges
    - Neutral wins
    - Neutral losses
  - Punish start/endings
  - Green: KO
  - Yellow: Drop
  - Red: Reversal
- Punish route
  - Mark each hit
  - Vector/trajectory (see if trajectory is feasible)
  - Number
  - Color

#### Example Code

```python
from treefrog.plot import plot, neutral_wins
from slippi.id import State

plot(neutral_wins(game, Stage.BATTLEFIELD, player="DTB#420")) # Heat map
```
