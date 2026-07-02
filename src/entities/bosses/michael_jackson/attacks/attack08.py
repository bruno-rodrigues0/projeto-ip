from re import L

import pygame
import math
from core import assets
from entities.enemy_attack import EnemyAttack, Projectile


S_LASER = pygame.Surface((40, 10))
S_LASER.fill((255, 255, 255))


class LaserProjectile(Projectile):
    vx = -300

    def move(self, dt: float, factor=1):
        self.ax -= 20 * factor * dt
        self.ay = 0


class Attack08(EnemyAttack):
    attack_time = 9
    running_time: float = 0.0


    def __init__(self) -> None:
        super().__init__()
        self.running_time = 0.0
        self.create_projectiles()


    def create_projectiles(self) -> None:

        for i in range(50):

            x = 900 + (i * 90)
            y = int(400 + math.sin(i) * 90)

            self.projectiles.append(LaserProjectile(S_LASER, x, y))


    def update(self, dt: float) -> None:

        for proj in self.projectiles:
            proj.move(dt)
            proj.update(dt)

        self.running_time += dt
