class gamestats:
  """track stats for alien invasion"""

  def __init__(self, ai_game):
    """initialize statistics"""
    self.setting = ai_game.settings
    self.reset_stats()
    self.high_score = 0
    self.level = 1

  def reset_stats(self):
    """initialize statistics that can change during the game"""
    self.ships_left = self.setting.ship_limit
    self.score = 0