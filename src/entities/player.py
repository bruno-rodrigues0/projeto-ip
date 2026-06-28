import pygame

from components.object import SimulatedObject
import core.assets as assets
from core.input import InputBuffer, InputState, Action

class PredRect:
    """
    Player movement prediction rect.
    """

    def __init__(self, rect):
        self.rect = rect

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
    INVINCIBILITY_TIME = 0.02

    def __init__(self, image, x, y, max_hp):
        super().__init__(image, x, y)
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.hp_percent = 1.0
        self.damage = self._initial_damage = 10
        self.defense = self._initial_defense = 10
        self._damage_buff_count = self._defense_buff_count = 0
        self._invincible_timer = 0.0


    def take_damage(self, amount: int) -> None:
        if self._invincible_timer > 0:
            return
        assets.SFX_MASTER.audios["damage_taken"].play()
        self.current_hp = int(max(0, self.current_hp - (amount - (self.defense / 100) * amount)))
        self.hp_percent = self.current_hp / self.max_hp
        self._invincible_timer = self.INVINCIBILITY_TIME


    def heal(self, amount):
        self.current_hp = int(min(self.max_hp, self.current_hp + amount))
        self.hp_percent = self.current_hp / self.max_hp


    def buff_damage(self, amount, buff_count):
        self.damage += amount
        self._damage_buff_count = buff_count


    def buff_defense(self, amount, buff_count):
        self.defense = min(100, self.defense + amount)
        self._defense_buff_count = buff_count

    def move(self, action_buffer: InputBuffer, arena: pygame.sprite.Group, vel: int, dt: float) -> None:
        # Move in X axis
        if (
            action_buffer[Action.RIGHT] == InputState.HELD
            and action_buffer[Action.LEFT] == InputState.NOTHING
        ):
            self.vx = vel
        elif (
            action_buffer[Action.LEFT] == InputState.HELD
            and action_buffer[Action.RIGHT] == InputState.NOTHING
        ):
            self.vx = -vel
        else:
            self.vx = 0

        next_pos = self.get_next_pos(dt)
        assert self.image is not None
        pred_rect = PredRect(self.image.get_rect(topleft=(next_pos[0], next_pos[1])))
        collided = pygame.sprite.spritecollide(pred_rect, arena, False)
        if collided:
            self.vx = 0

        # Move in Y axis
        if (
            action_buffer[Action.UP] == InputState.HELD
            and action_buffer[Action.DOWN] == InputState.NOTHING
        ):
            self.vy = -vel
        elif (
            action_buffer[Action.DOWN] == InputState.HELD
            and action_buffer[Action.UP] == InputState.NOTHING
        ):
            self.vy = vel
        else:
            self.vy = 0

        next_pos = self.get_next_pos(dt)
        pred_rect = PredRect(self.image.get_rect(topleft=(next_pos[0], next_pos[1])))
        collided = pygame.sprite.spritecollide(pred_rect, arena, False)
        if collided:
            self.vy = 0

    def update_buffs(self):
        if self._damage_buff_count > 0:
            self._damage_buff_count -= 1
            if self._damage_buff_count == 0:
                self.damage = self._initial_damage

        if self._defense_buff_count > 0:
            self._defense_buff_count -= 1
        if self._defense_buff_count == 0:
                self.defense = self._initial_defense

    def update(self, dt: float) -> None:
        super().update(dt)
        if self._invincible_timer > 0:
            self._invincible_timer -= dt

