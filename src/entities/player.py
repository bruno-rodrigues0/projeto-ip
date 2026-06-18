from components.object import SimulatedObject

class Player(SimulatedObject):
  max_hp: int
  current_hp: int
  hp_percent: float

  def __init__(self, image, x, y, max_hp):
    super().__init__(image, x, y)
    self.max_hp = max_hp
    self.current_hp = max_hp
    self.hp_percent = 1.0

  def take_damage(self, amount):
    self.current_hp = max(0, self.current_hp - amount)
    self.hp_percent = self.current_hp / self.max_hp