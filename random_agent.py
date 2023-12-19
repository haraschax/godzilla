import random

class PlayerStrategy:
    def yield_tokyo(self, me, other_player):
        return random.random() < 0.5
    
    def keep_dice(self, me, other_player, dice, reroll_n):
        return [random.random() < 0.5 for _ in range(len(dice))]