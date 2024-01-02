import random
from constants import PlayerState, DIESIDE
from typing import List

class PlayerStrategy:
  def yield_tokyo(self, me: PlayerState, other_player: PlayerState, dice: List[DIESIDE]):
    # TODO implement smart logic
    return True
    
  def keep_dice(self, me: PlayerState, other_player: PlayerState, dice: List[DIESIDE], reroll_n: int):
    # TODO implement smart logic
    return [True for _ in range(len(dice))]