import pygame
import math
import core.constants as const
import core.assets as assets

from components.animation import AnimationPlayer
from entities.enemy_attack import EnemyAttack, Projectile


class HalfMoonLaser(Projectile):

    def move(self, dt: float, running_time=0.0):
        self.x = const.WINDOW_CENTRE[0] - 90 + math.cos(2 * running_time) * 250
        self.y = const.WINDOW_CENTRE[1] + math.sin(4 * running_time) * 150

    def update(self, dt: float, animation: AnimationPlayer) -> None:
        super().update(dt)
        animation.update(dt)
        self.image = pygame.transform.flip(animation.get_frame(), True, False).convert_alpha()

class Attack11(EnemyAttack):
    attack_time = 10
    running_time = 0.0
    animation = AnimationPlayer("moonwalk", assets.S_SAW, .05)

    def __init__(self) -> None:
        super().__init__()
        self.running_time = 0.0

        self.projectiles.append(HalfMoonLaser(pygame.Surface((0, 0)), 0.0, 180))

    def update(self, dt: float):
        self.running_time += dt

        for proj in self.projectiles:
            if hasattr(proj, 'move'):
                proj.move(dt, self.running_time)

            proj.update(dt, self.animation)
