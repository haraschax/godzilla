 
import random
from dataclasses import dataclass
from typing import List
from constants import DIESIDE, MAX_HEALTH, VICTORY_PTS_WIN, DIE_COUNT

@dataclass
class PlayerState:
    health: int = 10
    victory_points: int = 0
    in_tokyo: bool = False

class Game:
    def __init__(self, player_strategies=[]):
        self.players = [PlayerState() for _ in range(2)]
        self.player_strategies = player_strategies
        assert len(self.player_strategies) == len(self.players)
        self.winner = -1
        self.current_player_idx = 0
    
    @property
    def n_players(self):
        return len(self.players)
    
    @property
    def current_player(self):
        return self.players[self.current_player_idx]
    
    @property
    def other_player_idx(self):
        return (self.current_player_idx + 1) % self.n_players

    @property
    def other_player(self):
      return self.players[self.other_player_idx]

    def other_player_yields_tokyo(self):
        return self.player_strategies[self.other_player_idx].yield_tokyo(self.other_player, self.current_player)

    def start_turn(self):
        if self.current_player.in_tokyo:
            self.current_player.victory_points += 2
    
    def roll_n_dice(self, n):
        return [random.choice([DIESIDE.ATTACK, DIESIDE.HEAL, DIESIDE.ONE, DIESIDE.TWO, DIESIDE.THREE]) for _ in range(n)]

    def roll_dice(self):
        dice_results = self.roll_n_dice(DIE_COUNT)
        for i in range(2):
            keep_mask = self.player_strategies[self.current_player_idx].keep_dice(self.current_player, self.other_player, dice_results, reroll_n=i)
            dice_results = [dice_results[i] for i in range(DIE_COUNT) if keep_mask[i]] + self.roll_n_dice(DIE_COUNT - sum(keep_mask))
        return dice_results

    def resolve_victory_point_dice(self, dice):
        for dieside in [DIESIDE.ONE, DIESIDE.TWO, DIESIDE.THREE]:
          cnt = sum([x == dieside for x in dice])
          if cnt >= 3:
            self.current_player.victory_points += int(dieside)
            self.current_player.victory_points += min(0, cnt - 3)

    def resolve_health_dice(self, dice):
        heals = sum([x == DIESIDE.HEAL for x in dice])
        if not self.current_player.in_tokyo:
          self.current_player.health  = min(MAX_HEALTH, self.current_player.health + heals)

    def resolve_attack_dice(self, dice):
        attack = sum([x == DIESIDE.ATTACK for x in dice])
        if self.current_player.in_tokyo:
          self.other_player.health  = self.other_player.health - attack
        elif self.other_player.in_tokyo:
          self.other_player.health  = self.other_player.health - attack
          if self.other_player_yields_tokyo():
            self.current_player.in_tokyo = True
            self.other_player.in_tokyo = False
        else:
            self.current_player.in_tokyo = True
            self.current_player.victory_points += 1


    def resolve_dice(self, dice):
        self.resolve_victory_point_dice(dice)
        self.resolve_health_dice(dice)
        self.resolve_attack_dice(dice)
    
    def check_winner(self):
        for i, player in enumerate(self.players):
            if player.health <= 0:
                self.winner = (i + 1) % self.n_players
            if player.victory_points >= VICTORY_PTS_WIN:
                self.winner = i

    def step(self):
        self.start_turn()
        dice = self.roll_dice()
        self.resolve_dice(dice)
        self.check_winner()
        self.current_player_idx = (self.current_player_idx + 1) % self.n_players
    
    def __str__(self):
        return (f'GAME STATE: player {self.tokyo_player_idx} is in tokyo \n' +
                f'Players 0 has {self.players[0].health} health and {self.players[0].victory_points} victory points \n' +  
                f'Players 1 has {self.players[1].health} health and {self.players[1].victory_points} victory points')


if __name__ == '__main__':
  import importlib
  import sys
  if len(sys.argv) != 3:
    print('Example usage: python game.py random_agent simple_agent')
    sys.exit(1)
  _, strategy_one, strategy_two =sys.argv
  module_one = importlib.import_module(strategy_one)
  module_two = importlib.import_module(strategy_two) 
  GAMES_N = 100
  winners = []
  for i in range(GAMES_N):
    game = Game(player_strategies=[module_one.PlayerStrategy(), module_two.PlayerStrategy()])
    while game.winner == -1:
      game.step()
    winners.append(game.winner)
  player_0_wins = sum([x == 0 for x in winners])
  print(f'{strategy_one} won {player_0_wins}/{GAMES_N} games against {strategy_two}')