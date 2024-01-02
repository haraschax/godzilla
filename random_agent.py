import random
from constants import PlayerState, DIESIDE
from typing import List

class PlayerStrategy:
  def yield_tokyo(self, me: PlayerState, other_player: PlayerState, dice: List[DIESIDE]):
    return random.random() < 0.5
    
  def keep_dice(self, me: PlayerState, other_player: PlayerState, dice: List[DIESIDE], reroll_n: int):
    return [random.random() < 0.5 for _ in range(len(dice))]