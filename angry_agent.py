import random
from constants import DIESIDE
from constants import MAX_HEALTH

class PlayerStrategy:
  def yield_tokyo(self, me, other_player):
    return me.health <= 5
        
  def keep_dice(self, me, other_player, dice, reroll_n):
    heals = 0
    to_heal = MAX_HEALTH - me.health
    keep_mask = []
    for die in dice:
      if die == DIESIDE.HEAL:
        if heals < to_heal and not me.in_tokyo:
          keep_mask.append(True)
          heals += 1
        else:
          keep_mask.append(False)
      elif die == DIESIDE.ATTACK:
        keep_mask.append(True)
      else:
        keep_mask.append(False)
    return keep_mask