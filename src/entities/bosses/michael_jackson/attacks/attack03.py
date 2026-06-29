import pygame

from core import assets
from entities.enemy_attack import EnemyAttack, Projectile


class Projectile01(Projectile):
    def move(self, dt:float, factor=1):
        self.ax -= 240 * factor * dt
        self.ay += 60 * factor * dt


class Projectile02(Projectile):
    def move(self, dt:float, factor=1):
        self.ax -= 600 * factor * dt
        self.ay += 180.5 * factor * dt


class Projectile03(Projectile):
    def move(self, dt:float, factor=1):
        self.ax -= 480 * factor * dt
        self.ay -= 240 * factor * dt


class Projectile04(Projectile):
    def move(self, dt:float, factor=1):
        self.ax += 300 * factor * dt
        self.ay -= 120 * factor * dt


class Projectile05(Projectile):
    def move(self, dt:float, factor=1):
        self.ax += 540 * factor * dt
        self.ay -= 30.5 * factor * dt


class Projectile06(Projectile):
    def move(self, dt:float, factor=1):
        self.ax += 180 * factor * dt
        self.ay += 120 * factor * dt


class Attack03(EnemyAttack):
    initial_time: int
    attack_time = 6
    running_time: float = 0.0

    def __init__(self) -> None:
        super().__init__()
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
                proj.move(dt)
            else:
                proj.move(dt, -1)
            proj.update(dt)

        self.running_time += dt
