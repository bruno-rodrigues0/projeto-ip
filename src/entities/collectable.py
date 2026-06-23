import pygame
import math

from components.object import SimulatedObject


class Collectable(SimulatedObject):
    type: str
    buff: int
    sound: pygame.mixer.Sound
    vy = 50
    x_ref: int

    def __init__(
        self,
        image: pygame.surface.Surface,
        x: float,
        y: float,
        type: str,
        buff: int,
        sound: pygame.mixer.Sound
    ) -> None:

        super().__init__(image, x, y)
        self.type = type
        self.buff = buff
        self.sound = sound

    def update(self, dt: float) -> None:
        super().update(dt)
        self.x = (self.x_ref + math.sin(self.y / 15) * (self.y // 10))

