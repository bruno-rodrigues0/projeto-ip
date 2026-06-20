from components.object import SimulatedObject
import core.assets as assets

class Player(SimulatedObject):
    """
    Player entity.
    """

    max_hp: int
    current_hp: int
    hp_percent: float
    _initial_damage: int
    damage: int
    _damage_buff_count: int
    _initial_defense: int
    defense: int
    _defense_buff_count: int
    def __init__(self, image, x, y, max_hp):
        super().__init__(image, x, y)
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.hp_percent = 1.0
        self.damage = self._initial_damage = 10
        self.defense = self._initial_defense = 10
        self._damage_buff_count = self._defense_buff_count = 0


    def take_damage(self, amount):
        assets.SFX_DAMAGE_TAKEN.play()
        self.current_hp = int(max(0, self.current_hp - (amount - (self.defense / 100) * amount)))
        self.hp_percent = self.current_hp / self.max_hp


    def heal(self, amount):
        self.current_hp = int(min(self.max_hp, self.current_hp + amount))
        self.hp_percent = self.current_hp / self.max_hp


    def buff_damage(self, amount, buff_count):
        self.damage += amount
        self._damage_buff_count = buff_count

    
    def buff_defense(self, amount, buff_count):
        self.defense = min(100, self.defense + amount)
        self._defense_buff_count = buff_count


    def update_buffs(self):
        if self._damage_buff_count > 0:
            self._damage_buff_count -= 1
            if self._damage_buff_count == 0:
                self.damage = self._initial_damage

        if self._defense_buff_count > 0:
            self._defense_buff_count -= 1
        if self._defense_buff_count == 0:
                self.defense = self._initial_defense

