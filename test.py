import unittest
from unittest.mock import patch, Mock
from game import Game, DIESIDE


class TestGame(unittest.TestCase):
  def setUp(self):
    self.mock_strategy = Mock()
    self.game = Game(player_strategies=[self.mock_strategy, self.mock_strategy])

  def test_initialization(self):
    self.assertEqual(self.game.n_players, 2)
    self.assertEqual(self.game.winner, -1)
    self.assertEqual(self.game.current_player_idx, 0)

  def test_start_turn(self):
    self.game.current_player.in_tokyo = True
    initial_points = self.game.current_player.victory_points
    self.game.start_turn()
    self.assertEqual(self.game.current_player.victory_points, initial_points + 2)

  def test_roll_dice(self):
    dice_outcomes = [DIESIDE.ATTACK] * 6 + [DIESIDE.HEAL] * 3 + [DIESIDE.THREE]
    with patch('game.random.choice', side_effect=dice_outcomes):
      keep_dice_masks = [
        [True, True, True, False, False, False],  # First roll keep mask
        [True, True, True, True, True, False]     # Second roll keep mask
      ]

      self.mock_strategy.keep_dice.side_effect = lambda *args, **kwargs: keep_dice_masks[kwargs['reroll_n']]

      dice_result = self.game.roll_dice()
    expected_dice_result = [DIESIDE.ATTACK] * 3 + [DIESIDE.HEAL] * 2 + [DIESIDE.THREE]
    self.assertEqual(dice_result, expected_dice_result)

  def test_resolve_victory_point_dice_allvps(self):
    initial_points = self.game.current_player.victory_points
    self.game.resolve_victory_point_dice([DIESIDE.ONE] * 6)
    self.assertEqual(self.game.current_player.victory_points, initial_points + 4)

  def test_resolve_victory_point_dice_novps(self):
    initial_points = self.game.current_player.victory_points
    self.game.resolve_victory_point_dice([DIESIDE.ATTACK] * 6)
    self.assertEqual(self.game.current_player.victory_points, initial_points)

  def test_resolve_victory_point_dice_lowvps_1(self):
    initial_points = self.game.current_player.victory_points
    self.game.resolve_victory_point_dice([DIESIDE.HEAL] * 4 + [DIESIDE.TWO] * 2)
    self.assertEqual(self.game.current_player.victory_points, initial_points)

  def test_resolve_victory_point_dice_lowvps_2(self):
    initial_points = self.game.current_player.victory_points
    self.game.resolve_victory_point_dice([DIESIDE.ONE] * 4 + [DIESIDE.TWO] * 2)
    self.assertEqual(self.game.current_player.victory_points, initial_points + 2)

  def test_resolve_victory_point_dice_vps(self):
    initial_points = self.game.current_player.victory_points
    self.game.resolve_victory_point_dice([DIESIDE.ONE] * 3 + [DIESIDE.THREE] * 3)
    self.assertEqual(self.game.current_player.victory_points, initial_points + 4)

  def test_resolve_health_dice_intokyo(self):
    self.game.current_player.in_tokyo = True
    self.game.current_player.health = 5
    dice = [DIESIDE.HEAL] * 3
    self.game.resolve_health_dice(dice)
    self.assertEqual(self.game.current_player.health, 5)

  def test_resolve_health_dice_notintokyo(self):
    self.game.current_player.in_tokyo = False
    self.game.current_player.health = 5
    dice = [DIESIDE.HEAL] * 3
    self.game.resolve_health_dice(dice)
    self.assertEqual(self.game.current_player.health, 8)

  def test_resolve_attack_dice_notintokyo(self):
    self.game.current_player.in_tokyo = False
    self.game.other_player.in_tokyo = True
    self.game.other_player.health = 10
    dice = [DIESIDE.ATTACK] * 3
    self.mock_strategy.yield_tokyo.return_value = True
    self.game.resolve_attack_dice(dice)
    self.assertEqual(self.game.other_player.health, 7)
    self.assertEqual(self.game.current_player.in_tokyo, True)

  def test_resolve_attack_dice_tokyo(self):
    self.game.current_player.in_tokyo = True
    self.game.other_player.in_tokyo = False
    self.game.other_player.health = 10
    dice = [DIESIDE.ATTACK] * 3
    self.game.resolve_attack_dice(dice)
    self.assertEqual(self.game.other_player.health, 7)

  def test_resolve_attack_dice_notokyo(self):
    self.game.current_player.in_tokyo = False
    self.game.other_player.in_tokyo = False
    dice = [DIESIDE.ATTACK] * 3
    initial_points = self.game.current_player.victory_points
    self.game.resolve_attack_dice(dice)
    self.assertEqual(self.game.current_player.in_tokyo, True)
    self.assertEqual(self.game.current_player.victory_points, initial_points + 1)

  def test_check_winner_by_health(self):
    self.game.players[0].health = 0
    self.game.check_winner()
    self.assertEqual(self.game.winner, 1)

  def test_check_winner_by_victory_points(self):
    self.game.players[0].victory_points = 20
    self.game.check_winner()
    self.assertEqual(self.game.winner, 0)

  def test_step(self):
    initial_player_idx = self.game.current_player_idx
    self.mock_strategy.keep_dice.side_effect = [[True] * 6] * 3
    self.game.step()
    self.assertNotEqual(self.game.current_player_idx, initial_player_idx)


if __name__ == '__main__':
  unittest.main()
