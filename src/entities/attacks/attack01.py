import pygame

from core import assets
from entities.enemy_attack import EnemyAttack, Projectile
    

class Projectile01(Projectile):
    def move(self) -> None:
        self.ax += 10


class Projectile02(Projectile):
    def move(self) -> None:
        self.ax -= 10


class Attack01(EnemyAttack):
    initial_time: int
    attack_time = 2

    def __init__(self) -> None:
        self.initial_time = pygame.time.get_ticks()
        self.create_projectiles()

    def create_projectiles(self) -> None:
        for i in range(4):
            projectile = Projectile01(assets.S_CIRCLE_ATTACK, 400 - 30 * i, 320 + 60 * i)
            projectile.ax = 20 * (i + 1)
            self.projectiles.append(projectile)

        for i in range(3):
            projectile = Projectile02(assets.S_CIRCLE_ATTACK, 800 + 30 * i, 350 + 60 * i)
            projectile.ax = -1 * (20 * (i + 1))
            self.projectiles.append(projectile)

    def update(self, dt: float) -> None:
        for proj in self.projectiles:
            proj.move()
            proj.update(dt)
