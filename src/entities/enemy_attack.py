import pygame

from abc import abstractmethod
from components.object import SimulatedObject


class Projectile(SimulatedObject):
    def __init__(self, image: pygame.surface.Surface, x: float, y: float) -> None:
        super().__init__(image, x, y)

    @abstractmethod
    def move(self) -> None: ...

class EnemyAttack:
    projectiles: list[Projectile] = []
    attack_time: int
    finished: bool

    @abstractmethod
    def update(self, dt: float) -> None: ...
