import pygame

from core import assets
from entities.enemy_attack import EnemyAttack, Projectile


class Projectile01(Projectile):
    def move(self, factor=1):
        self.ax -= 4 * factor
        self.ay += 1 * factor


class Projectile02(Projectile):
    def move(self, factor=1):
        self.ax -= 10 * factor
        self.ay += 3.5 * factor


class Projectile03(Projectile):
    def move(self, factor=1):
        self.ax -= 8 * factor
        self.ay -= 4 * factor


class Projectile04(Projectile):
    def move(self, factor=1):
        self.ax += 5 * factor
        self.ay -= 2 * factor


class Projectile05(Projectile):
    def move(self, factor=1):
        self.ax += 9 * factor
        self.ay -= 0.5 * factor


class Projectile06(Projectile):
    def move(self, factor=1):
        self.ax += 3 * factor
        self.ay += 2 * factor


class Attack03(EnemyAttack):
    initial_time: int
    attack_time = 6
    running_time: float = 0.0

    def __init__(self) -> None:
        self.initial_time = pygame.time.get_ticks()
        self.running_time = 0.0
        self.create_projectiles()


    def create_projectiles(self) -> None:
        self.projectiles.append(Projectile01(assets.S_AYUWOKI_ATTACK, 800, 320))
        self.projectiles.append(Projectile02(assets.S_CRESCENDO_ATTACK, 820, 380))
        self.projectiles.append(Projectile03(assets.S_AUW_ATTACK, 810, 440))
        self.projectiles.append(Projectile04(assets.S_ANNIE_ATTACK, 400, 430))
        self.projectiles.append(Projectile05(assets.S_SMOOTH_ATTACK, 410, 370))
        self.projectiles.append(Projectile06(assets.S_CRESCENDO_ATTACK, 390, 310))


    def update(self, dt: float) -> None:
        for proj in self.projectiles:
            if self.running_time < 1.1:
                proj.move()
            else:
                proj.move(-1)
            proj.update(dt)

        self.running_time += dt
